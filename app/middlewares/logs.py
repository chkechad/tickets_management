"""logging middleware."""

import logging
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):  # type: ignore[misc]
    """logging middleware."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Dispatch the request and log the method, url, status code and duration."""
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time
        logger.info(
            f"Middleware Tickets: Méthode={request.method} URL={request.url.path} "
            f"Statut={response.status_code} Durée={duration:.3f}s"
        )
        return response
