from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import logic.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter('logic.routing.websocket_urlpatterns')
    )
}
)