from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from .models import User, Chat, ChatParticipant, Message, MessageReadReceipt
from .serializers import UserSerializer, ChatSerializer, ChatParticipantSerializer, MessageSerializer, \
    MessageReadReceiptSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(tags=["Users"], operation_description="Retrieve all users", operation_id='ListUsers')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"], operation_description="Create a new user", operation_id='CreateUser')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"], operation_description="Retrieve a single user", operation_id='RetrieveUser')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"], operation_description="Update a user", operation_id='UpdateUser')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"], operation_description="Partially update a user",
                         operation_id='PartialUpdateUser')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"], operation_description="Delete a user", operation_id='DeleteUser')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @swagger_auto_schema(tags=["Chats"], operation_description="Retrieve all chats", operation_id='ListChats')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chats"], operation_description="Create a new chat", operation_id='CreateChat')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chats"], operation_description="Retrieve a single chat", operation_id='RetrieveChat')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chats"], operation_description="Update a chat", operation_id='UpdateChat')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chats"], operation_description="Partially update a chat",
                         operation_id='PartialUpdateChat')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chats"], operation_description="Delete a chat", operation_id='DeleteChat')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class ChatParticipantViewSet(viewsets.ModelViewSet):
    queryset = ChatParticipant.objects.all()
    serializer_class = ChatParticipantSerializer

    @swagger_auto_schema(tags=["Chat Participants"], operation_description="Retrieve all chat participants",
                         operation_id='ListChatParticipants')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chat Participants"], operation_description="Create a new chat participant",
                         operation_id='CreateChatParticipant')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chat Participants"], operation_description="Retrieve a single chat participant",
                         operation_id='RetrieveChatParticipant')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chat Participants"], operation_description="Update a chat participant",
                         operation_id='UpdateChatParticipant')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chat Participants"], operation_description="Partially update a chat participant",
                         operation_id='PartialUpdateChatParticipant')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chat Participants"], operation_description="Delete a chat participant",
                         operation_id='DeleteChatParticipant')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @swagger_auto_schema(tags=["Messages"], operation_description="Retrieve all messages", operation_id='ListMessages')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Messages"], operation_description="Create a new message", operation_id='CreateMessage')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Messages"], operation_description="Retrieve a single message",
                         operation_id='RetrieveMessage')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Messages"], operation_description="Update a message", operation_id='UpdateMessage')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Messages"], operation_description="Partially update a message",
                         operation_id='PartialUpdateMessage')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Messages"], operation_description="Delete a message", operation_id='DeleteMessage')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class MessageReadReceiptViewSet(viewsets.ModelViewSet):
    queryset = MessageReadReceipt.objects.all()
    serializer_class = MessageReadReceiptSerializer

    @swagger_auto_schema(tags=["Message Read Receipts"], operation_description="Retrieve all message read receipts",
                         operation_id='ListMessageReadReceipts')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Message Read Receipts"], operation_description="Create a new message read receipt",
                         operation_id='CreateMessageReadReceipt')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Message Read Receipts"], operation_description="Retrieve a single message read receipt",
                         operation_id='RetrieveMessageReadReceipt')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Message Read Receipts"], operation_description="Update a message read receipt",
                         operation_id='UpdateMessageReadReceipt')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Message Read Receipts"],
                         operation_description="Partially update a message read receipt",
                         operation_id='PartialUpdateMessageReadReceipt')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Message Read Receipts"], operation_description="Delete a message read receipt",
                         operation_id='DeleteMessageReadReceipt')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

