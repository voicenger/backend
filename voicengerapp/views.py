from rest_framework import viewsets

from .models import Chat, Message, UserChat
from .serializers import ChatSerializer, MessageSerializer, UserChatSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserChatViewSet(viewsets.ModelViewSet):
    queryset = UserChat.objects.all()
    serializer_class = UserChatSerializer
