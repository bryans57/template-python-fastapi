import os
import sys

from fastapi import FastAPI

from src.conf import Container
from src.infrastructure.api.middleware import (
    add_middlewares,
    global_exception_handler,
    lifespan,
    log_requests,
)
from src.infrastructure.api.routers.index import routes
from src.util import Enviroments


sys.path.append(os.path.abspath("src"))
print(sys.path)  # This should include the absolute path to `src`

# Dependency Container Configuration
Container()
app = FastAPI(lifespan=lifespan, docs_url=f"{Enviroments.PREFIX}/docs")

# Middlewares Config
add_middlewares(app)

# Middleware for logging requests and responses
app.middleware("http")(log_requests)

# Routes Registration
app.include_router(routes, prefix=Enviroments.PREFIX)
print("PREFIX = " + Enviroments.PREFIX)

# Global Exception Handler Registration
app.add_exception_handler(Exception, global_exception_handler)
