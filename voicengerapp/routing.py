# routing.py

from django.urls import re_path

from voicengerapp.consumers.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chats/$', ChatConsumer.as_asgi()),
]
