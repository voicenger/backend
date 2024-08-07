from django.urls import path
from . import consumers
from .consumers import APIGatewayConsumer

websocket_urlpatterns = [
    path('ws/api_gateway/', APIGatewayConsumer.as_asgi()),
]
