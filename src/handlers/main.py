"""Centralized Lambda handler - routes all requests to appropriate handlers."""

import json
import re
import time

from src.handlers.health.check import health_check
from src.handlers.requests.list import list_requests
from src.handlers.requests.create import create_request
from src.handlers.requests.get import get_request
from src.handlers.requests.delete import delete_request
from src.handlers.requests.update import update_request
from src.handlers.requests.list_user_requests import list_user_requests
from src.handlers.favorites.create import create_favorite
from src.handlers.favorites.delete import delete_favorite
from src.handlers.favorites.list import list_user_favorites
from src.lib.responses import error


# Routes: (method, path_pattern, handler)
ROUTES = [
    # Health
    ("GET", "/health", health_check),
    # Requests
    ("GET", "/v0/requests", list_requests),
    ("POST", "/v0/requests", create_request),
    ("GET", "/v0/requests/{request_id}", get_request),
    ("DELETE", "/v0/requests/{request_id}", delete_request),
    ("PATCH", "/v0/requests/{request_id}", update_request),
    ("GET", "/v0/users/{user_id}/requests", list_user_requests),
    # Favorites
    ("POST", "/v0/favorites", create_favorite),
    ("DELETE", "/v0/favorites/{favorite_id}", delete_favorite),
    ("GET", "/v0/favorites", list_user_favorites),
]


def _path_to_regex(path: str) -> re.Pattern:
    """Convert path pattern like /v0/requests/{request_id} to regex."""
    pattern = re.escape(path)
    pattern = re.sub(r"\\{(\w+)\\}", r"(?P<\1>[^/]+)", pattern)
    return re.compile(f"^{pattern}$")


# Pre-compile route patterns at module load time
COMPILED_ROUTES = [
    (method, _path_to_regex(path), route_handler)
    for method, path, route_handler in ROUTES
]


def handler(event, context):
    """Main entry point - routes to appropriate handler."""
    start = time.perf_counter()
    method = event["requestContext"]["http"]["method"]
    path = event["rawPath"]

    response = None
    matched_route = None

    try:
        for route_method, pattern, route_handler in COMPILED_ROUTES:
            if method == route_method:
                match = pattern.match(path)
                if match:
                    matched_route = route_handler.__name__
                    if match.groupdict():
                        event.setdefault("pathParameters", {}).update(match.groupdict())
                    response = route_handler(event, context)
                    return response

        response = error("Not found", status_code=404)
        return response
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        status = response.get("statusCode", 500) if response else 500
        print(json.dumps({
            "request_id": context.aws_request_id,
            "app_route": matched_route or "not_found",
            "app_method": method,
            "app_path": path,
            "app_status": status,
            "app_duration_ms": round(duration_ms, 2),
        }))
