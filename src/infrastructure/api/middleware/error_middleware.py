import json
import traceback

from datetime import (
    datetime,
    timezone,
)

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.domain.exceptions.errorcode import ErrorCode


class CustomException(Exception):
    def __init__(self, message: str, cause: str = None, code: ErrorCode = ErrorCode.UNKNOWN_ERROR):
        self.message = message
        self.cause = cause
        self.code = code


def build_error_response(
    error: Exception,
    cause: str = None,
    status_code: int = 500,
    error_code: ErrorCode = ErrorCode.UNKNOWN_ERROR.value,
):
    return {
        "isError": True,
        "message": str(error),
        "code": getattr(error, "code", error_code),
        "cause": cause or traceback.format_exc(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "statusCode": status_code,
    }


def translate_error(error: Exception):
    if isinstance(error, SyntaxError):
        return build_error_response(error, "Syntax error in JSON", 500, ErrorCode.SYNTAX_ERROR.value)
    if isinstance(error, CustomException):
        return build_error_response(error, error.cause)
    if isinstance(error, ValidationError):
        return {
            "statusCode": 422,
            "message": "Validation error",
            "details": json.loads(error.json()),
        }
    if isinstance(error, ValueError):
        return build_error_response(error, "ValueError")
    return build_error_response(error, "Default translator error", 500, ErrorCode.UNKNOWN_ERROR.value)


async def global_exception_handler(request: Request, exc: Exception):
    exception = translate_error(exc)
    return JSONResponse(
        status_code=exception["statusCode"],
        content={**exception, "id": getattr(request.state, "id", None)},
    )
