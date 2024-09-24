from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse 
from user_transactions.models.http import HttpErrorResponse
from uuid import  uuid4

import time

class RequestDataMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            process_time: float = 0
            request.state.request_id = str(uuid4())
            
            start_time = time.perf_counter()
            response = await call_next(request)
            
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response
            
        except Exception as e:
            
            response = JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=HttpErrorResponse(request_data=request.state.request_data,
                                                          error_details=f"Unexpected error processing request {e}",
                                                          retryable=False).model_dump())
            
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return 