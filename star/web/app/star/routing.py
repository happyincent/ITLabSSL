from channels.routing import ProtocolTypeRouter, URLRouter

import edge.routing
from edge.token_auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    
    # 'websocket':  URLRouter(
    #     edge.routing.websocket_urlpatterns
    # ),

    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            edge.routing.websocket_urlpatterns
        )
    ),
})