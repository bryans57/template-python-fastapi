import json
import os

from typing import (
    Any,
    Dict,
)

from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import _StreamingResponse
from starlette.responses import FileResponse


MAX_BODY_LENGTH = 1024  # Define appropriate length


# Middleware for CORS y HTTPS Redirect
def add_middlewares(app: FastAPI):
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this for the domain in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Middleware for logging requests and responses
async def log_requests(request: Request, call_next):
    # Capture the request body
    request_body = await request.body()
    try:
        request_body_json = json.loads(request_body)
    except ValueError:
        request_body_json = {}

    # Capture the response
    response = await call_next(request)
    truncated_body = b""

    # If a FileResponse is ever handled, validate the typing to ensure functionality
    if isinstance(response, (FileResponse, _StreamingResponse)):
        # Assemble the response body from the iterator without modifying the response
        body = b"".join([chunk async for chunk in response.body_iterator])

        # Log a truncated version for large responses
        truncated_body = body[:MAX_BODY_LENGTH] + (b"... [truncated]" if len(body) > MAX_BODY_LENGTH else b"")
    else:
        # For plain Response or JSONResponse, body is available directly
        body = response.body
        truncated_body = body[:MAX_BODY_LENGTH] + (b"... [truncated]" if len(body) > MAX_BODY_LENGTH else b"")

    log_data = {
        "application": os.getenv("APP_NAME", "template-python-fastapi"),
        "id": (str(request.state.request_id) if hasattr(request.state, "request_id") else None),
        "method": request.method,
        "url": str(request.url),
        "request": {
            "headers": dict(request.headers),
            "body": request_body_json,
            "params": request.path_params,
            "query": dict(request.query_params),
        },
        "response": {
            "statusCode": response.status_code,
            "payload": (
                truncated_body.decode("utf-8", errors="replace")
                if truncated_body
                else body.decode("utf-8", errors="replace")
            ),
        },
    }

    print(json.dumps(log_data))

    # Recreate the body iterator for StreamingResponse types
    if isinstance(response, _StreamingResponse):

        async def new_body_iterator():
            yield body

        response.body_iterator = new_body_iterator()

    return response


def parse(data: str) -> Dict[str, Any]:
    return json.loads(data)
