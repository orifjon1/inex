import sys
import os


from django.core.asgi import get_asgi_application

from task import middlewares
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from config.routing import websocket_urlpatterns

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": middlewares.WebSocketJWTAuthMiddleware(

            URLRouter(
                websocket_urlpatterns))
    }
)
