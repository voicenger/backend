from rest_framework import viewsets, generics
from .models import User, Chat, ChatParticipant, Message, MessageReadReceipt, GroupChat, GroupChatParticipant, GroupChatFile, GroupChatLink
from .serializers import UserSerializer, ChatSerializer, ChatParticipantSerializer, MessageSerializer, MessageReadReceiptSerializer, GroupChatSerializer, GroupChatParticipantSerializer, GroupChatFileSerializer, GroupChatLinkSerializer, RegisterSerializer, ProfileUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# ViewSet для пользователей
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ViewSet для чатов
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

# ViewSet для участников чатов
class ChatParticipantViewSet(viewsets.ModelViewSet):
    queryset = ChatParticipant.objects.all()
    serializer_class = ChatParticipantSerializer

# ViewSet для сообщений
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# ViewSet для квитанций о прочтении сообщений
class MessageReadReceiptViewSet(viewsets.ModelViewSet):
    queryset = MessageReadReceipt.objects.all()
    serializer_class = MessageReadReceiptSerializer

# ViewSet для групповых чатов
class GroupChatViewSet(viewsets.ModelViewSet):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer

# ViewSet для участников групповых чатов
class GroupChatParticipantViewSet(viewsets.ModelViewSet):
    queryset = GroupChatParticipant.objects.all()
    serializer_class = GroupChatParticipantSerializer

# ViewSet для файлов групповых чатов
class GroupChatFileViewSet(viewsets.ModelViewSet):
    queryset = GroupChatFile.objects.all()
    serializer_class = GroupChatFileSerializer

# ViewSet для ссылок на групповые чаты
class GroupChatLinkViewSet(viewsets.ModelViewSet):
    queryset = GroupChatLink.objects.all()
    serializer_class = GroupChatLinkSerializer

# Представление для регистрации
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Представление для обновления профиля
class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
