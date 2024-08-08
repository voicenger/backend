import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import websocket
from websocket import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voicenger.settings.development')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(

            websocket.routing.websocket_urlpatterns
        )
    ),
})