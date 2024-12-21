from .common_middleware import (
    add_middlewares,
    log_requests,
)
from .error_middleware import global_exception_handler
from .verification_db import lifespan
