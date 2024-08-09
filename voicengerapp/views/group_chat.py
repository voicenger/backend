from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..serializers import GroupChatSerializer, GroupChatParticipantSerializer, GroupChatFileSerializer, GroupChatLinkSerializer
from ..models import GroupChat, GroupChatParticipant, GroupChatFile, GroupChatLink

# ViewSet для групповых чатов
class GroupChatViewSet(viewsets.ModelViewSet):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]

# ViewSet для участников групповых чатов
class GroupChatParticipantViewSet(viewsets.ModelViewSet):
    queryset = GroupChatParticipant.objects.all()
    serializer_class = GroupChatParticipantSerializer
    permission_classes = [IsAuthenticated]

# ViewSet для файлов групповых чатов
class GroupChatFileViewSet(viewsets.ModelViewSet):
    queryset = GroupChatFile.objects.all()
    serializer_class = GroupChatFileSerializer
    permission_classes = [IsAuthenticated]

# ViewSet для ссылок на групповые чаты
class GroupChatLinkViewSet(viewsets.ModelViewSet):
    queryset = GroupChatLink.objects.all()
    serializer_class = GroupChatLinkSerializer
    permission_classes = [IsAuthenticated]
