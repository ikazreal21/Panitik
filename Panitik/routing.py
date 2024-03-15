from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import lms.routing

application = ProtocolTypeRouter(
    {'websocket': AuthMiddlewareStack(URLRouter(lms.routing.websocket_urlpatterns))}
)
