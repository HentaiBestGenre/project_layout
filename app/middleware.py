from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

import logging
import logging.config
import datetime as dt

import time
import json
from typing import Callable

from utils import AsyncIteratorWrapper


class RouterLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, *, logger: logging.Logger) -> None:
        self._logger = logger
        super().__init__(app)
   
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        logging_dict = {}

        response, response_dict = await self._log_response(call_next, request)
        request_dict = await self._log_request(request)
        logging_dict["correlation_id"] = response.headers['x-request-id']
        logging_dict["request"] = request_dict
        logging_dict["response"] = response_dict
        logging_dict["datetime"] = dt.datetime.now()

        self._logger.info(logging_dict)

        return response

    async def _log_request( self, request: Request ) -> str:
            path = request.url.path
            if request.query_params:
                path += f"?{request.query_params}"

            request_logging = {
                "method": request.method,
                "path": path,
                "ip": request.client.host
            }

            try:
                body = await request.json()
                request_logging["body"] = body
            except:
                body = None

            return request_logging
    
    async def _log_response(self, call_next: Callable, request: Request) -> list[Response, dict]:
        start_time = time.perf_counter()
        response = await self._execute_request(call_next, request)
        finish_time = time.perf_counter()

        overall_status = "successful" if  response.status_code < 400 else "failed"
        execution_time = finish_time - start_time

        response.headers["time_taken"] = f"{execution_time:0.4f}"
        response_logging = {
            "status": overall_status,
            "status_code": response.status_code,
            "time_taken": f"{execution_time:0.4f}s"
        }

        if response.__dict__.get("body_iterator"):
            resp_body = [section async for section in response.__dict__["body_iterator"]]
            response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))

            try:
                resp_body = json.loads(resp_body[0].decode())
            except:
                resp_body = str(resp_body)

            response_logging["body"] = resp_body
        else:
            response_logging["body"] = response.body.decode()

        return response, response_logging

    async def _execute_request(self, call_next: Callable, request: Request) -> Response:
        try:
            response: Response = await call_next(request)
            response.headers["x-request-id"] = request.headers['x-request-id']
            return response
        except HTTPException as e:
            self._logger.exception(
                {
                    "path": request.url.path,
                    "method": request.method,
                    "reason": str(e),
                    "correlation_id": request.headers['x-request-id']
                }
            )
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": str(e.detail)},
                headers={"x-request-id": request.headers['x-request-id']}
            )

        except Exception as e:
            self._logger.exception(
                {
                    "path": request.url.path,
                    "method": request.method,
                    "reason": str(e),
                    "correlation_id": request.headers['x-request-id']
                }
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal Server Error"},
                headers={"x-request-id": request.headers['x-request-id']}
            )


class MaxBodySizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_body_size: int):
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request: Request, call_next):
        request_body_length = int(request.headers.get('content-length', 0))
        if request_body_length > self.max_body_size:
            return JSONResponse(content={"detail": "Request body too large"}, status_code=413)
        return await call_next(request)
