from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

from .models import Chat, Message, UserChat
from .serializers import ChatSerializer, MessageSerializer, UserChatSerializer, RegisterSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserChatViewSet(viewsets.ModelViewSet):
    queryset = UserChat.objects.all()
    serializer_class = UserChatSerializer


class RegisterView(generics.CreateAPIView):
    queryset = UserChat.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
