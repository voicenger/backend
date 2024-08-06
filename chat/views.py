from rest_framework import viewsets
from .models import GroupChat, GroupChatParticipant, GroupChatFile, GroupChatLink
from .serializers import GroupChatSerializer, GroupChatParticipantSerializer, GroupChatFileSerializer, \
    GroupChatLinkSerializer


class GroupChatViewSet(viewsets.ModelViewSet):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer


class GroupChatParticipantViewSet(viewsets.ModelViewSet):
    queryset = GroupChatParticipant.objects.all()
    serializer_class = GroupChatParticipantSerializer


class GroupChatFileViewSet(viewsets.ModelViewSet):
    queryset = GroupChatFile.objects.all()
    serializer_class = GroupChatFileSerializer


class GroupChatLinkViewSet(viewsets.ModelViewSet):
    queryset = GroupChatLink.objects.all()
    serializer_class = GroupChatLinkSerializer
