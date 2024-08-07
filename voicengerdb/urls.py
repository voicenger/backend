from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ChatViewSet, ChatParticipantViewSet, MessageViewSet, MessageReadReceiptViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'chat-participants', ChatParticipantViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'message-read-receipts', MessageReadReceiptViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
]
