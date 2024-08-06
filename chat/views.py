from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from .models import GroupChat, GroupChatParticipant, GroupChatFile, GroupChatLink
from .serializers import GroupChatSerializer, GroupChatParticipantSerializer, GroupChatFileSerializer, \
    GroupChatLinkSerializer


class GroupChatViewSet(viewsets.ModelViewSet):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer

    @swagger_auto_schema(tags=["Group Chats"], operation_description="Retrieve all group chats", operation_id='ListGroupChats')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chats"], operation_description="Create a new group chat", operation_id='CreateGroupChat')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chats"], operation_description="Retrieve a single group chat", operation_id='RetrieveGroupChat')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chats"], operation_description="Update a group chat", operation_id='UpdateGroupChat')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chats"], operation_description="Partially update a group chat", operation_id='PartialUpdateGroupChat')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chats"], operation_description="Delete a group chat", operation_id='DeleteGroupChat')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GroupChatParticipantViewSet(viewsets.ModelViewSet):
    queryset = GroupChatParticipant.objects.all()
    serializer_class = GroupChatParticipantSerializer

    @swagger_auto_schema(tags=["Group Chat Participants"], operation_description="Retrieve all group chat participants", operation_id='ListGroupChatParticipants')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Participants"], operation_description="Create a new group chat participant", operation_id='CreateGroupChatParticipant')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Participants"], operation_description="Retrieve a single group chat participant", operation_id='RetrieveGroupChatParticipant')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Participants"], operation_description="Update a group chat participant", operation_id='UpdateGroupChatParticipant')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Participants"], operation_description="Partially update a group chat participant", operation_id='PartialUpdateGroupChatParticipant')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Participants"], operation_description="Delete a group chat participant", operation_id='DeleteGroupChatParticipant')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GroupChatFileViewSet(viewsets.ModelViewSet):
    queryset = GroupChatFile.objects.all()
    serializer_class = GroupChatFileSerializer

    @swagger_auto_schema(tags=["Group Chat Files"], operation_description="Retrieve all group chat files", operation_id='ListGroupChatFiles')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Files"], operation_description="Create a new group chat file", operation_id='CreateGroupChatFile')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Files"], operation_description="Retrieve a single group chat file", operation_id='RetrieveGroupChatFile')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Files"], operation_description="Update a group chat file", operation_id='UpdateGroupChatFile')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Files"], operation_description="Partially update a group chat file", operation_id='PartialUpdateGroupChatFile')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Files"], operation_description="Delete a group chat file", operation_id='DeleteGroupChatFile')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GroupChatLinkViewSet(viewsets.ModelViewSet):
    queryset = GroupChatLink.objects.all()
    serializer_class = GroupChatLinkSerializer

    @swagger_auto_schema(tags=["Group Chat Links"], operation_description="Retrieve all group chat links", operation_id='ListGroupChatLinks')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Links"], operation_description="Create a new group chat link", operation_id='CreateGroupChatLink')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Links"], operation_description="Retrieve a single group chat link", operation_id='RetrieveGroupChatLink')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Links"], operation_description="Update a group chat link", operation_id='UpdateGroupChatLink')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Links"], operation_description="Partially update a group chat link", operation_id='PartialUpdateGroupChatLink')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Group Chat Links"], operation_description="Delete a group chat link", operation_id='DeleteGroupChatLink')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
