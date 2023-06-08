import os

from django.core.asgi import get_asgi_application

from config.middlewares import WebSocketJWTAuthMiddleware
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from config.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": WebSocketJWTAuthMiddleware(

            URLRouter(
                websocket_urlpatterns))
    }
)
