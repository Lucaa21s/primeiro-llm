import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import Response
try:
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
except Exception:
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"
    Counter = None
    Histogram = None
    generate_latest = None

from app.core.logger import logger

REQUEST_COUNT = (
    Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
    if Counter
    else None
)

REQUEST_LATENCY = (
    Histogram("http_request_duration_seconds", "HTTP request latency in seconds", ["method", "path"])
    if Histogram
    else None
)


def register_observability(app: FastAPI):
    @app.middleware("http")
    async def metrics_and_logging_middleware(request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        start = time.perf_counter()

        response = await call_next(request)

        duration = time.perf_counter() - start
        path = request.url.path
        method = request.method
        status = str(response.status_code)

        if REQUEST_COUNT is not None:
            REQUEST_COUNT.labels(method=method, path=path, status=status).inc()
        if REQUEST_LATENCY is not None:
            REQUEST_LATENCY.labels(method=method, path=path).observe(duration)

        response.headers["x-request-id"] = request_id
        logger.info(
            "request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
            request_id,
            method,
            path,
            status,
            duration * 1000,
        )
        return response

    @app.get("/metrics")
    async def metrics_endpoint():
        if generate_latest is None:
            return Response("prometheus_client not installed\n", media_type="text/plain")
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
