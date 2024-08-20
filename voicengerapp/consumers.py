from channels.db import database_sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from voicengerapp.massage import GetChatsMessage, CreateEmptyChatMessage, JoinChatMessage, GetChatDetailsMessage


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    async def connect(self):
        user = self.scope.get('user')

        if user and user.is_authenticated:
            self.user = user
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        """
        Processes incoming data via WebSocket.
        """
        if text_data is not None:
            text_data_json = json.loads(text_data)
            command = text_data_json.get('command')
            if command == 'getChats':
                await self.handle_get_chats()
            elif command == 'emptyChatCreated':
                await self.handle_create_empty_chat(text_data_json)
            elif command == 'joinChat':
                await self.handle_join_chat(text_data_json)
            elif command == 'getChatDetails':
                chat_id = text_data_json.get('chat_id')
                await self.handle_get_chat_detail(chat_id)
        if bytes_data is not None:
            pass

    async def handle_get_chats(self):
        """
        Handles a request to retrieve the list of chats.

        Note:
        This method does not accept input data or return any values.
        """
        try:
            chats = await self.get_all_chats()
            serialized_chats = await self.serialize_chats(chats)
            message = GetChatsMessage(serialized_chats=serialized_chats)
            await self.send(text_data=json.dumps(message.to_dict()))
        except Exception as e:
            error_message = {
                "type": "error",
                'message': str(e)
            }
            await self.send(text_data=json.dumps(error_message))

    async def handle_get_chat_detail(self, chat_id: int):
        """
        Handles a request to retrieve the details of a specific chat.
        """
        chat = await self.get_chat(chat_id)
        if chat is None:
            error_message = {
                'type': 'error',
                'message': 'Chat not found'
            }
            await self.send(text_data=json.dumps(error_message))
            return
        serialized_chat = await self.serialize_chat(chat)
        message = GetChatDetailsMessage(serialized_chat=serialized_chat)
        await self.send(text_data=json.dumps(message.to_dict()))

    async def handle_create_empty_chat(self, data):
        """
        Handles the creation of a new chat.

        This method processes incoming data to create a new chat and optionally add participants to it.
        """
        from voicengerapp.serializers import ChatSerializer
        participants_ids = data.get('participants', [])
        chat_data = {
            'participants': participants_ids
        }
        serializer_chat = ChatSerializer(data=chat_data)

        if not serializer_chat.is_valid():
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid data',
                'errors': serializer_chat.errors
            }))
            return

        chat = await self.create_chat()

        if participants_ids:
            await self.add_participants_to_chat(chat.id, participants_ids)

        chat_data = await self.serialize_chat(chat)

        message = CreateEmptyChatMessage(
            chat_id=chat_data['id'],
            participants=chat_data['participants'],
            created_at=chat_data['created_at'],
            updated_at=chat_data['updated_at'],
        )
        await self.send(text_data=json.dumps(message.to_dict()))

    async def handle_join_chat(self, data):
        """
        Processes a request to join a chat and displays the latest message.
        """
        chat_id = data.get('chat_id')
        last_read_message_id = data.get('last_read_message', None)

        user = self.scope["user"]

        chat = await self.get_chat(chat_id)
        if chat is None:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Chat not found'
            }))
            return

        is_participant = await self.is_user_in_chat(user=user, chat=chat)
        if is_participant:
            await self.send(text_data=json.dumps({
                'type': 'info',
                'message': 'You are already in the chat'
            }))
            return

        await self.add_participants_to_chat(chat_id=chat_id, participants_ids=[user.id])

        last_message_data = await self.get_last_message(chat_id=chat_id)

        message = JoinChatMessage(
            chat_id=chat_id,
            last_read_message=last_read_message_id if last_read_message_id else None,
            last_message=last_message_data
        )
        await self.send(text_data=json.dumps(message.to_dict()))

    @database_sync_to_async
    def get_all_chats(self):
        from voicengerapp.models import Chat
        return Chat.objects.all()

    @database_sync_to_async
    def serialize_chats(self, chats):
        from voicengerapp.serializers import ChatSerializer
        serializer = ChatSerializer(chats, many=True)
        return serializer.data

    @database_sync_to_async
    def serialize_chat(self, chat):
        from voicengerapp.serializers import ChatSerializer
        serializer = ChatSerializer(chat)
        return serializer.data

    @database_sync_to_async
    def create_chat(self):
        from voicengerapp.models import Chat
        chat = Chat.objects.create()
        return chat

    @database_sync_to_async
    def add_participants_to_chat(self, chat_id: int, participants_ids: list[int]):
        from voicengerapp.models import Chat
        from django.contrib.auth.models import User
        try:
            chat = Chat.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            return {'error': 'Chat not found'}

        for participant_id in participants_ids:
            try:
                user = User.objects.get(id=participant_id)
                chat.participants.add(user)
            except ObjectDoesNotExist:
                continue
        chat.save()
        return chat

    @database_sync_to_async
    def is_user_in_chat(self, user, chat):
        return chat.participants.filter(id=user.id).exists()

    @database_sync_to_async
    def get_chat(self, chat_id):
        from voicengerapp.models import Chat
        try:
            return Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return None

    @database_sync_to_async
    def get_user(self, user_id: int):
        from django.contrib.auth.models import User
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def get_last_message(self, chat_id):
        from voicengerapp.models import Message
        from voicengerapp.serializers import MessageSummarySerializer

        try:
            message = Message.objects.filter(chat_id=chat_id).latest('timestamp')
            serializer = MessageSummarySerializer(message)
            return serializer.data
        except Message.DoesNotExist:
            return None
