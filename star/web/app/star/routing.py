from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import tx2.routing

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            tx2.routing.websocket_urlpatterns
        )
    ),
    # 'websocket':  URLRouter(
    #     tx2.routing.websocket_urlpatterns
    # ),
})