"""Registrar las requests.
"""
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

audit_logger = logging.getLogger("audit.http")

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        user_id = getattr(request.state, "user_id", None)
        role = getattr(request.state, "user_role", None)

        audit_logger.info("HTTP_REQUEST", extra={
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_ip": request.client.host if request.client else None,
            "user_id": user_id,
            "role": role,
        })

        response = await call_next(request)

        audit_logger.info("HTTP_RESPONSE", extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "user_id": user_id,
        })
        return response