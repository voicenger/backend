# routing.py

from django.urls import re_path

from .consumers import Token

websocket_urlpatterns = [
    re_path(r'ws/token/$', Token.as_asgi()),
]
