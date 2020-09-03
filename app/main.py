import logging
import uuid
import time
from typing import Any

import rapidjson
import structlog
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()


# Clear Gunicorn access log to remove duplicate requests logging
logging.getLogger("gunicorn.access").handlers.clear()

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.threadlocal.merge_threadlocal,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(serializer=rapidjson.dumps, sort_keys=True),
    ],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    cache_logger_on_first_use=True,
)
log = structlog.get_logger()


@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    # clear the threadlocal context
    structlog.threadlocal.clear_threadlocal()
    # bind threadlocal
    structlog.threadlocal.bind_threadlocal(
        logger="uvicorn.access",
        request_id=str(uuid.uuid4()),
        cookies=request.cookies,
        scope=request.scope,
        url=str(request.url),
    )
    try:
        start_time = time.time()
        response: Response = await call_next(request)
    finally:
        process_time = time.time() - start_time
        log.info(
            "processed a request",
            status_code=response.status_code,
            process_time=process_time,
        )
    return response


@app.get("/ping", response_class=PlainTextResponse)
def ping() -> Any:
    return "pong"
