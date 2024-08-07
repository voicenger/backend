from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ChatViewSet, ChatParticipantViewSet, MessageViewSet, MessageReadReceiptViewSet, GroupChatViewSet, GroupChatParticipantViewSet, GroupChatFileViewSet, GroupChatLinkViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'chat-participants', ChatParticipantViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'message-read-receipts', MessageReadReceiptViewSet)
router.register(r'group-chats', GroupChatViewSet)
router.register(r'group-chat-participants', GroupChatParticipantViewSet)
router.register(r'group-chat-files', GroupChatFileViewSet)
router.register(r'group-chat-links', GroupChatLinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
