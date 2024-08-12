from django.urls import re_path

from .consumers import UserMessageConsumer

websocket_urlpatterns = [
    re_path(r'ws/universal/$', UserMessageConsumer.as_asgi()),
]
