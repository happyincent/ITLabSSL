from urllib.parse import parse_qs
from django.db import close_old_connections

from channels.auth import AuthMiddlewareStack

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()

        params = parse_qs(scope['query_string'].decode('utf-8'))
        scope['token'] = params.get('token')[0] if params.get('token') else None

        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))