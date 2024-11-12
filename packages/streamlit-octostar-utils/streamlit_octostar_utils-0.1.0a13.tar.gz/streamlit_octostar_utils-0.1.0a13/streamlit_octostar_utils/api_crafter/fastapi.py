import asyncio
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Literal, Any
from io import BytesIO
import zipfile
from abc import ABC, abstractmethod
import json
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import ast
import uuid
from functools import wraps
import traceback
from copy import copy

MAX_ERROR_MESSAGE_BYTES = 256
MAX_ERROR_TRACEBACK_BYTES = 10240
DEFAULT_PROCESSOR_SUFFIX = 'main'


class CommonParsers(object):
    async def parse_form_list(form_data: str,
                              format=Literal['csv', 'python']) -> Optional[List[str]]:
        try:
            if not form_data:
                return None
            if format == 'csv':
                return form_data.split(',')
            elif format == 'python':
                return ast.literal_eval(form_data)
        except BaseException as e:
            raise ValidationError(f"Parsing failed in parse_from_list: {str(e.__class__)} {str(e)}")

class Route(ABC):
    def route(route, **route_kwargs):
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            func_name = func.__name__
            if asyncio.iscoroutinefunction(func):
                wrapper = async_wrapper
            else:
                wrapper = sync_wrapper
            func_name = func.__name__
            wrapper._route_kwargs = route_kwargs
            wrapper._route_funcname = func_name
            route.routed_funcs.append(wrapper)
            return wrapper
        return decorator
    
    def include(route):
        def decorator(func):
            func_name = func.__name__
            if getattr(route, func_name, None):
                raise ValueError(f"Cannot have two FastAPI routes with the same name {func_name} within the same Route!")
            setattr(route, func_name, func)
            return func
        return decorator

    def __init__(self, app, router=None):
        self.app = app
        self._router = router
        self.routed_funcs = []
        self.define_routes()
    
    @abstractmethod
    def define_routes(self):
        pass
    
    @property
    def router(self):
        return self._router or self.app
    
    def include_routes(self, router_mapping=None):
        for func in self.routed_funcs:
            route_kwargs = copy(func._route_kwargs)
            router = self.router
            if route_kwargs.get('router'):
                router = route_kwargs['router']
            elif router_mapping:
                router = router_mapping.get(func._route_funcname, self.router)
            else:
                router = self.router
            route_kwargs.pop('router', None)
            router.add_api_route(
                **route_kwargs,
                endpoint=func
            )
        return self
        
class CommonModels(object):
    class OKResponseModel(BaseModel):
        message: str = "OK"
        status: str = "success"

    class DataResponseModel(BaseModel):
        data: Any
        status: str = "success"

    class ZipResponseModel(object):
        class Element(object):
            def __init__(self, file: bytes, path: str, filename: str, json: dict):
                self.file = file
                self.path = path
                self.filename = filename
                self.json = json

        def __init__(self, elements: List[Element], paths: Optional[List[str]] = None, filename: Optional[str] = None, status: str = "success"):
            self.elements = elements
            self.paths = paths
            self.status = status
            self.filename = filename

        def get(self):
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for element in self.elements:
                    file_name = f"{element.path}/{element.filename}"
                    zip_file.writestr(file_name, element.file)
                    json_name = f"{element.path}/{element.filename}.dict"
                    zip_file.writestr(json_name, json.dumps(element.json, indent=4))
                for path in self.paths:
                    zip_file.writestr(path + "/", '')
                zip_file.writestr('response.dict', json.dumps({'status': self.status}, indent=4))
            zip_buffer.seek(0)
            headers = {}
            headers['Content-Disposition'] = 'attachment;'
            filename = self.filename or (str(uuid.uuid4()) + ".zip")
            headers['Content-Disposition'] += f' filename="{filename}"'
            return StreamingResponse(zip_buffer, media_type='application/zip', headers=headers)


class DefaultErrorRoute(Route):
    error_responses = {
        500: {
            "description": "Generic Server Error",
            "content": {
                "application/json": {
                    "example": {"message": "Something unexpected went wrong!", "status": "error"}
                }
            }
        },
        501: {
            "description": "Not Implemented",
            "content": {
                "application/json": {
                    "example": {"message": "This method (with these parameters) is not implemented!", "status": "error"}
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {"message": "These two lists must have the same length!", "status": "error"}
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {"message": "Validation error on 0 -> filename!", "status": "error"}
                }
            }
        },
    }

    def format_error(exc, body=bytes(), debug=False):
        '''Generic Error Handler'''
        status_code = 500
        if isinstance(exc, StarletteHTTPException):
            status_code = exc.status_code
        elif isinstance(exc, NotImplementedError):
            status_code = 501
        elif isinstance(exc, AssertionError):
            status_code = 400
        elif isinstance(exc, ValidationError) or isinstance(exc, RequestValidationError):
            status_code = 422
        try:
            message = exc.message
        except:
            message = str(exc)
        if debug:
            message += "\n" + str(body)
        if len(message) > MAX_ERROR_MESSAGE_BYTES:
            message = message[-MAX_ERROR_MESSAGE_BYTES:]
        try:
            tcbk = traceback.format_exception(exc)
            if len(tcbk) > MAX_ERROR_TRACEBACK_BYTES:
                tcbk = tcbk[-MAX_ERROR_TRACEBACK_BYTES:]
        except:
            tcbk = None
        response_content = {"message": message, 'status': 'error'}
        if debug:
            response_content['traceback'] = tcbk
        return JSONResponse(
            status_code=status_code,
            content=response_content
        )

    async def handle_error(body: bytes, exc: Exception, debug: bool):
        return DefaultErrorRoute.format_error(exc, body, debug=debug)

    def add_default_exceptions_handler(fs_app, debug=False):
        async def async_handle_error(request: Request, exc: Exception):
            return await DefaultErrorRoute.handle_error(request, exc, debug)

        fs_app.add_exception_handler(RequestValidationError, async_handle_error)
        fs_app.add_exception_handler(StarletteHTTPException, async_handle_error)
        fs_app.add_exception_handler(Exception, async_handle_error)


class RequestCancelledMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        queue = asyncio.Queue()

        async def message_poller(sentinel, handler_task):
            nonlocal queue
            while True:
                message = await receive()
                if message["type"] == "http.disconnect":
                    handler_task.cancel()
                    return sentinel
                await queue.put(message)
        sentinel = object()
        handler_task = asyncio.create_task(self.app(scope, queue.get, send))
        asyncio.create_task(message_poller(sentinel, handler_task))
        try:
            return await handler_task
        except asyncio.CancelledError:
            print("Cancelling request due to disconnect")