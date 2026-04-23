from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.custom_exceptions import (
    EmptyInputException,
    LLMTimeoutException,
    LLMServiceException
)

def register_exception_handlers(app: FastAPI):
    
    @app.exception_handler(EmptyInputException)
    async def empty_input_exception_handler(request: Request, exc: EmptyInputException):
        return JSONResponse(
            status_code=400
            , content={
                "detail":exc.message
                , "error_type": "EMPTY_INPUT"
            }
        )
    
    @app.exception_handler(LLMTimeoutException)
    async def llm_timeout_exception_handler(request: Request, exc: LLMTimeoutException):
        return JSONResponse(
            status_code=504,
            content={
                "detail": exc.message,
                "error_type": "LLM_TIMEOUT"
            }
        )

    @app.exception_handler(LLMServiceException)
    async def llm_service_exception_handler(request: Request, exc: LLMServiceException):
        return JSONResponse(
            status_code=502,
            content={
                "detail": exc.message,
                "error_type": "LLM_SERVICE_ERROR"
            }
        )
    