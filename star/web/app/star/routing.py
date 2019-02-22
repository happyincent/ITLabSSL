from channels.routing import ProtocolTypeRouter, URLRouter

import tx2.routing
from tx2.token_auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    
    # 'websocket':  URLRouter(
    #     tx2.routing.websocket_urlpatterns
    # ),

    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            tx2.routing.websocket_urlpatterns
        )
    ),
})