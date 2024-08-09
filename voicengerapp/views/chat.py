from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from ..serializers import ChatSerializer, ChatParticipantSerializer
from ..models import Chat, ChatParticipant

# ViewSet для чатов
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat = serializer.save()
        if ChatParticipant.objects.filter(chat=chat).count() > 2:
            chat.delete()
            raise ValidationError("A chat can only have two participants.")

# ViewSet для участников чатов
class ChatParticipantViewSet(viewsets.ModelViewSet):
    queryset = ChatParticipant.objects.all()
    serializer_class = ChatParticipantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat = serializer.validated_data['chat']
        if ChatParticipant.objects.filter(chat=chat).count() >= 2:
            raise ValidationError("A chat can only have two participants.")
        serializer.save()
