from src.domain.exceptions.errorcode import (
    ErrorCode,
    StatusCode,
)


class ExceptionBase(Exception):
    def __init__(self, message: str, code: ErrorCode, status_code: StatusCode, cause: str = None):
        self.is_error = True
        self.message = message
        self.code = code
        self.status_code = status_code
        self.cause = cause or None

    def to_dict(self):
        return {
            "isError": self.is_error,
            "message": self.message,
            "code": self.code.value,
            "statusCode": self.status_code.value,
            "cause": self.cause,
        }


class AcceptedException(ExceptionBase):
    def __init__(self, cause: str, message: str):
        super().__init__(message, ErrorCode.REPOSITORY_ERROR, StatusCode.NO_CONTENT, cause)


class BadMessageException(ExceptionBase):
    def __init__(
        self,
        cause: str,
        message="The data entered does not match the defined schema",
        ok=False,
    ):
        super().__init__(message, ErrorCode.BAD_MESSAGE, StatusCode.OK if ok else StatusCode.BAD_REQUEST, cause)


class DatabaseErrorHandling(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception

    def __str__(self):
        return f"Database error: {self.original_exception}"
