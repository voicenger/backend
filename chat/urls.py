from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupChatViewSet, GroupChatParticipantViewSet, GroupChatFileViewSet, GroupChatLinkViewSet

router = DefaultRouter()
router.register(r'group-chats', GroupChatViewSet)
router.register(r'group-chat-participants', GroupChatParticipantViewSet)
router.register(r'group-chat-files', GroupChatFileViewSet)
router.register(r'group-chat-links', GroupChatLinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
