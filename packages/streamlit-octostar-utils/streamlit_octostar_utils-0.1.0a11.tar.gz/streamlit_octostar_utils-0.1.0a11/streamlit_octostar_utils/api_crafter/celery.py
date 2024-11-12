from pathlib import Path
from celery import Celery
from celery.result import AsyncResult
import celery.signals as celery_signals
from kombu import Queue
from abc import ABC, abstractmethod
import asyncio
import subprocess
from fastapi import Query
import time
import os
import pickle
import atexit
import redis
import uuid
import json
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
import logging
logger = logging.getLogger(__name__)

from .fastapi import Route, CommonModels, DefaultErrorRoute

class CeleryQueueConfig:
    def __init__(self, n_workers=os.cpu_count(), max_tasks_per_child=None, max_memory_per_child=None, **options):
        self.n_workers = n_workers
        self.max_tasks_per_child = max_tasks_per_child
        self.max_memory_per_child = max_memory_per_child # KiB
        self.options = options

class CelerySerialized:
    def __init__(self, folder, data=None):
        if not data:
            data = {}
        self.folder = folder
        self.data = data
    
    def set_task_id(self, task_id):
        self.task_id = task_id
    
    def dump(self):
        assert(self.task_id)
        with open(os.path.join(self.folder, self.task_id), "wb") as target_file:
            return pickle.dump(self.data, file=target_file, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        assert(self.task_id)
        with open(os.path.join(self.folder, self.task_id), "rb") as source_file:
            data = pickle.load(source_file)
        return data

class CeleryExecutor(object):
    AWAITING = "AWAITING"
    MAX_STARTUP_CHECKS = 20
    CELERY_BROKER_PREFIX = "celery-task-meta-"
    BACKEND_COMM_THREADS_RATIOS = {
        'get': 50,
        'set': 20,
        'io': 30
    }

    def __init__(self, name, module_name, base_folder=os.getcwd(), cleanup_every_secs=(3600, 300), queue_config=None, loglevel='info'):
        # Basic info
        self.name = name
        self.loglevel = loglevel
        self.base_folder = base_folder
        self.filename = module_name
        self.queue_config = queue_config or {"default": CeleryQueueConfig()}
        self.n_workers = sum(queue.n_workers for queue in self.queue_config.values())
        
        # Helper threadpools setup
        self.get_thread_pool = None
        self.set_thread_pool = None
        self.io_thread_pool = None
        
        # Folder setup
        root = Path(base_folder).resolve().joinpath('data')
        self.out_folder = root.joinpath('out')
        self.in_folder = root.joinpath('in')
        shutil.rmtree(root, ignore_errors=True)
        for folder in [self.in_folder, self.out_folder]:
            os.makedirs(folder, exist_ok=True)
        
        # Redis config
        self.redis_host = "127.0.0.1"
        self.redis_port = 6379
        self.redis_process = None
        
        # Celery basic config
        self.app = Celery(self.filename)
        self.app.conf.broker_url = f'redis://{self.redis_host}:{self.redis_port}/0'
        self.app.conf.result_backend = f'redis://{self.redis_host}:{self.redis_port}/1'
        self.app.conf.track_started = True
        self.app.conf.task_serializer = 'json'
        self.app.conf.result_serializer = 'json'
        self.app.conf.accept_content = ['application/json']
        self.app.conf.result_expires = cleanup_every_secs[0]
        self.app.conf.backend_cleanup_schedule = cleanup_every_secs[1]
        self.app.conf.beat_max_loop_interval = cleanup_every_secs[1]
        
        # Queues setup
        self.preload_functions = {}
        self.resource_registry = {}
        self.app.conf.task_queues = [
            Queue(name, routing_key=name) for name in self.queue_config.keys()
        ]
        self.app.conf.task_default_queue = "default"
        self.app.conf.task_default_routing_key = "default"
        
        # Celery Executor setup
        self.processes = []
        self.beat_process = None
        self.stop_event = threading.Event()
        atexit.register(self.close)
        self.set_cleanup_task()

    def finalize(self):
        self.register_worker_initialization()

    def preload_on_worker_init(self, **kwargs):
        queue = os.environ.get('CELERY_WORKER_QUEUES', '')
        if queue in self.preload_functions:
            logger.warning(f"Preloading resources for queue {queue}")
            for preload_func in self.preload_functions[queue]:
                if queue not in self.resource_registry:
                    self.resource_registry[queue] = {}
                self.resource_registry[queue] = {**self.resource_registry[queue], **(preload_func())}

    def register_worker_initialization(self):
        celery_signals.worker_process_init.connect(self.preload_on_worker_init)

    @staticmethod
    def cleanup_task_results(in_dir, out_dir, redis_host, redis_port):
        logging.info("Running cleanup task!")
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port)
        cursor = 0
        while True:
            cursor, keys = redis_client.scan(cursor=cursor, match=CeleryExecutor.CELERY_BROKER_PREFIX + "*")
            if not keys:
                break
            for key in keys:
                ttl = redis_client.ttl(key)
                if ttl == -2 or ttl <= 0:
                    redis_client.delete(key)
                    task_id = key.decode().replace("celery-task-meta-", "")
                    if os.path.isfile(os.path.join(in_dir, task_id)):
                        os.remove(os.path.join(in_dir, task_id))
                    if os.path.isfile(os.path.join(out_dir, task_id)):
                        os.remove(os.path.join(out_dir, task_id))
                    logger.info(f"Deleted expired task result: {task_id}")
            if cursor == 0:
                break
        logger.info("Completed cleanup of expired task results.")

    def set_cleanup_task(self):
        self.app.task(CeleryExecutor.cleanup_task_results, name='celery.backend_cleanup')
        self.app.conf.beat_schedule = {
            'celery.backend_cleanup': {
                'task': 'celery.backend_cleanup',
                'schedule': self.app.conf.backend_cleanup_schedule,
                'args': (str(self.in_folder), str(self.out_folder), self.redis_host, self.redis_port)
            },
        }

    def start(self):
        logger.info("Starting Redis server...")
        self.redis_process = subprocess.Popen(['redis-server', '--bind', str(self.redis_host), '--port', str(self.redis_port)])
        redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port)
        attempts_done = 0
        while attempts_done < CeleryExecutor.MAX_STARTUP_CHECKS:
            try:
                redis_client.ping()
                break
            except:
                pass
                attempts_done += 1
                time.sleep(1.0)
            if attempts_done == CeleryExecutor.MAX_STARTUP_CHECKS:
                raise TimeoutError("Redis not ready after a long wait!")
        redis_client.flushall()
        for queue, queue_config in self.queue_config.items():
            worker_name = f'celery@{self.name}:{queue}'
            command = [
                'env', f'PYTHONPATH={os.getcwd()}', f'CELERY_WORKER_QUEUES={queue}',
                'celery', '--app', f'{self.filename}.{self.name}', 'worker',
                f'--loglevel={self.loglevel}', f'--concurrency={queue_config.n_workers}', f'-n {worker_name}'
            ]
            if queue_config.max_tasks_per_child is not None:
                command.append(f'--max-tasks-per-child={queue_config.max_tasks_per_child}')
            if queue_config.max_memory_per_child is not None:
                command.append(f'--max-memory-per-child={queue_config.max_memory_per_child}')
            process = subprocess.Popen(command)
            self.processes.append(process)
        self.beat_process = subprocess.Popen([
            'celery', '--app', f'{self.filename}.{self.name}', 'beat', f'--loglevel={self.loglevel}'
        ])
        attempts_done = 0
        while attempts_done < CeleryExecutor.MAX_STARTUP_CHECKS:
            print("Waiting for Celery workers to become ready...")
            try:
                inspector = self.app.control.inspect()
                active_workers = inspector.active()
                if active_workers and len(active_workers) == len(self.processes):
                    print("Celery is ready!")
                    break
            except:
                pass
            attempts_done += 1
            time.sleep(1.0)
            if attempts_done == CeleryExecutor.MAX_STARTUP_CHECKS:
                raise TimeoutError("Celery not ready after a long wait!")
        total_ratio = sum(CeleryExecutor.BACKEND_COMM_THREADS_RATIOS.values())
        normalized_ratios = {key: value / total_ratio for key, value in CeleryExecutor.BACKEND_COMM_THREADS_RATIOS.items()}
        allocated_workers = {key: round(self.n_workers * ratio) for key, ratio in normalized_ratios.items()}
        while sum(allocated_workers.values()) != self.n_workers:
            diff = self.n_workers - sum(allocated_workers.values())
            key = max(allocated_workers, key=lambda k: normalized_ratios[k] - (allocated_workers[k] / self.n_workers))
            allocated_workers[key] += diff
        assert(all(workers > 0 for workers in allocated_workers.values()))
        self.get_thread_pool = ThreadPoolExecutor(max_workers=allocated_workers['get'])
        self.set_thread_pool = ThreadPoolExecutor(max_workers=allocated_workers['set'])
        self.io_thread_pool = ThreadPoolExecutor(max_workers=allocated_workers['io'])

    def close(self):
        if self.processes:
            logger.info("Terminating Celery...")
            for process in self.processes:
                process.terminate()
                process.wait()
                self.processes = []
        if self.beat_process:
            self.beat_process.terminate()
            self.beat_process.wait()
        if self.redis_process:
            logger.info("Stopping Redis server...")
            self.redis_process.terminate()
            self.redis_process.wait()
            self.redis_process = None

    def serialized_io(self, task_fn):
        @wraps(task_fn)
        def wrapper(task):
            task_id = task.request.id
            serialized_data = CelerySerialized(folder=self.in_folder)
            serialized_data.set_task_id(task_id)
            data = serialized_data.load()
            del serialized_data
            args, kwargs = data.get("args", []), data.get("kwargs", {})
            out_data = task_fn(task, *args, **kwargs)
            serialized_data = CelerySerialized(folder=self.out_folder, data=out_data)
            serialized_data.set_task_id(task_id)
            serialized_data.dump()
            del serialized_data
            if os.path.isfile(os.path.join(self.in_folder, task_id)):
                os.remove(os.path.join(self.in_folder, task_id))
            return task_id
        return wrapper
    
    @staticmethod
    def base_task(celery_executor, *args, **opts):
        def decorator(func):
            @wraps(func)
            def wrapper(task, *task_args, **task_kwargs):
                task.request.resources = celery_executor.resource_registry or {}
                return func(task, *task_args, **task_kwargs)
            serialized_func = celery_executor.serialized_io(wrapper)
            task_func = celery_executor.app.task(*args, **opts)(serialized_func)
            return task_func
        return decorator

    @staticmethod
    def preload(celery_executor, queue='default', *args, **opts):
        def decorator(func):
            if queue not in celery_executor.preload_functions:
                celery_executor.preload_functions[queue] = []
            celery_executor.preload_functions[queue].append(func)
            return func
        return decorator

    async def send_task(self, task_fn, args=[], kwargs={}, **options) -> str:
        def _write_task_data(in_folder, task_args, task_kwargs, task_id):
            serialized_data = CelerySerialized(folder=in_folder, data={"args": task_args, "kwargs": task_kwargs})
            serialized_data.set_task_id(task_id)
            serialized_data.dump()
        def _send_task(celery_app, task_name, task_id, options):
            logger.info(f"Sending task {task_id}")
            celery_app.send_task(task_name, task_id=task_id, queue='tika+ocr', **options)
            result = AsyncResult(task_id, app=celery_app)
            result.backend.store_result(task_id, result=None, state=CeleryExecutor.AWAITING)
        task_id = str(uuid.uuid4())
        try:
            await asyncio.get_running_loop().run_in_executor(self.io_thread_pool, _write_task_data,
                self.in_folder, args, kwargs, task_id
            )
            await asyncio.get_running_loop().run_in_executor(self.set_thread_pool, _send_task,
                self.app, task_fn.name, task_id, options
            )
        except asyncio.CancelledError:
            logger.info(f"Cancelling task {task_id} due to disconnect!")
            await self.terminate_task(task_id)
            raise
        return task_id
    
    async def terminate_task(self, task_id):
        def _terminate_task(celery_app, task_id):
            celery_app.control.revoke(task_id, terminate=True)
        def _remove_task_data(celery_app, in_folder, out_folder, task_id):
            celery_app.AsyncResult(task_id).forget()
            if os.path.isfile(os.path.join(in_folder, task_id)):
                os.remove(os.path.join(in_folder, task_id))
            if os.path.isfile(os.path.join(out_folder, task_id)):
                os.remove(os.path.join(out_folder, task_id))
        await asyncio.get_running_loop().run_in_executor(self.set_thread_pool, _terminate_task,
            self.app, task_id
        )
        await asyncio.get_running_loop().run_in_executor(self.io_thread_pool, _remove_task_data,
            self.app, self.in_folder, self.out_folder, task_id
        )
    
    async def poll_task_state(self, task_id):
        def _poll_task_state(celery_app, task_id):
            task = celery_app.AsyncResult(task_id)
            ready, state = task.ready(), task.state
            return ready, state
        return await asyncio.get_running_loop().run_in_executor(self.get_thread_pool, _poll_task_state,
            self.app, task_id
        )
        
    async def get_task_result(self, task_id, remove=False):
        def _try_get_task_data(celery_app, task_id):
            celery_app.AsyncResult(task_id).get() # will raise if the task raised an exception
        def _read_task_data(out_folder, task_id):
            serialized_data = CelerySerialized(out_folder)
            serialized_data.set_task_id(task_id)
            result = serialized_data.load()
            return result
        def _remove_task_data(celery_app, in_folder, out_folder, task_id):
            celery_app.AsyncResult(task_id).forget()
            if os.path.isfile(os.path.join(in_folder, task_id)):
                os.remove(os.path.join(in_folder, task_id))
            if os.path.isfile(os.path.join(out_folder, task_id)):
                os.remove(os.path.join(out_folder, task_id))
        await asyncio.get_running_loop().run_in_executor(self.get_thread_pool, _try_get_task_data,
            self.app, task_id
        )
        result = await asyncio.get_running_loop().run_in_executor(self.get_thread_pool, _read_task_data,
            self.out_folder, task_id
        )
        if remove:
            await asyncio.get_running_loop().run_in_executor(self.get_thread_pool, _remove_task_data,
                self.app, self.in_folder, self.out_folder, task_id
            )
        return result
    
    async def send_and_wait_task(self, task_fn, args=[], kwargs={}, **options):
        task_id = await self.send_task(task_fn, args, kwargs, **options)
        ready = False
        state = None
        while not ready:
            ready, state = await self.poll_task_state(task_id)
            if state == "PENDING":
                raise ValueError("Task with given ID does not exist!")
            await asyncio.sleep(0.5)
        return await self.get_task_result(task_id, remove=True)

class FastAPICeleryTaskRoute(Route):
    def __init__(self, app, celery_executor, router=None):
        self.app = app
        self._router = router
        self.routed_funcs = []
        self.celery_executor = celery_executor
        self.define_routes()
    
    def define_routes(self):
        @Route.include(self)
        @Route.route(self, path="/task/{task_id}", methods=["DELETE"], summary='Cancel a queued or running task.',
            status_code=200, responses=DefaultErrorRoute.error_responses)
        async def delete_task(
            task_id: str
        ) -> CommonModels.OKResponseModel:
            await self.celery_executor.terminate_task(task_id)
            return CommonModels.OKResponseModel()

        @Route.include(self)
        @Route.route(self, path="/task/{task_id}", methods=["GET"], summary='Get task status (and result if available).',
            status_code=200, responses=DefaultErrorRoute.error_responses)
        async def get_task(
            task_id: str,
            pop: bool = Query(False)
        ) -> CommonModels.DataResponseModel:
            logger.info("Polling task status!")
            ready, state = await self.celery_executor.poll_task_state(task_id)
            if ready:
                logger.info("Getting task status!")
                try:
                    result = await self.celery_executor.get_task_result(task_id, remove=pop)
                except BaseException as e:
                    exc = e
            data = {}
            if state in ["FAILURE", "RETRY", "REVOKED"]:
                error_response = DefaultErrorRoute.format_error(exc, debug=True).body.decode('utf-8')
                data = {"task_state": state, "task_id": task_id, "data": json.loads(error_response)}
            elif state == "PENDING":
                data = {"task_state": "UNKNOWN", "task_id": task_id}
            elif state in ["AWAITING", "STARTED"]:
                data = {"task_state": state, "task_id": task_id}
            elif state == "SUCCESS":
                data = {"task_state": state, "task_id": task_id, "data": result}
            elif state == "STARTED":
                data = {"task_status": state, "task_id": task_id}
            else:
                raise ValueError(f"Unknown task state {state}!")
            return CommonModels.DataResponseModel(data=data)
            
class CeleryRoute(Route, ABC):
    def __init__(self, app, celery_executor, router=None, async_router=None):
        self.app = app
        self.celery_executor = celery_executor
        self._router = router
        self._async_router = async_router
        self.routed_funcs = []
        self.define_preloads()
        self.define_tasks()
        self.define_routes()
    
    @property
    def async_router(self):
        return self._async_router or self.app
    
    @abstractmethod  
    def define_tasks(self):
        pass
    
    def define_preloads(self):
        pass