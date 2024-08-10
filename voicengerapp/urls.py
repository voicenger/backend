from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ChatViewSet, MessageViewSet, UserChatViewSet

router = DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'userchats', UserChatViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', include(router.urls)),
]
