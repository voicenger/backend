from datetime import datetime, timedelta
from typing import Any
from channels.db import database_sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date
from django.utils import timezone
from voicengerapp.massage import GetChatsMessage, CreateEmptyChatMessage, JoinChatMessage, GetChatDetailsMessage, \
    NewMessage
import logging

logger = logging.getLogger('voicenger')


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
            elif command == 'createEmptyChat':
                await self.handle_create_empty_chat(text_data_json)
            elif command == 'joinChat':
                await self.handle_join_chat(text_data_json)
            elif command == 'getChatDetails':
                chat_id = text_data_json.get('chat_id')
                if chat_id is None:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'Chat ID is required.'
                    }))
                    return
                await self.handle_get_chat_detail(chat_id)
            elif command == 'newMessage':
                await self.handle_create_new_message(text_data_json)
            elif command == 'getChatMessages':
                await self.handle_get_chat_messages(text_data_json.get('data', {}))
        else:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid command.'
            }))
        if bytes_data is not None:
            pass

    async def handle_get_chat_messages(self, data: dict[str, Any]) -> None:
        """
        Handles the retrieval of messages from a chat with optional filtering by date and/or limit.
        """
        chat_id = data.get('chatId')
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        last = data.get('last')

        if not chat_id:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Chat ID is required.'
            }))
            return

        try:
            chat = await self.get_chat(chat_id)
            if not chat:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Chat not found.'
                }))
                return
            messages = await self.get_messages(chat_id, date_from, date_to, last)
            serialized_messages = await self.serialize_messages(messages)
            await self.send(text_data=json.dumps({
                'command': 'chatMessages',
                'data': serialized_messages
            }))
        except Exception as e:
            logger.error(f"Error handling chat messages for chat_id {chat_id}: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'An error occurred while retrieving messages. Please try again later.'
            }))

    async def handle_get_chats(self) -> None:
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
            logger.error(f"Error retrieving chats: {e}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "An error occurred while retrieving chats. Please try again later."
            }))

    async def handle_get_chat_detail(self, chat_id: int) -> None:
        """
        Handles a request to retrieve the details of a specific chat.
        """
        try:
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
        except Exception as e:
            logger.error(f"Error retrieving chat details for chat_id {chat_id}: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'An error occurred while retrieving chat details. Please try again later.'
            }))

    async def handle_create_empty_chat(self, data: dict[str, Any]) -> None:
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

        try:
            chat = await self.create_chat()
        except Exception as e:
            logger.error(f"Could not create chat: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Could not create chat. Please try again later.'
            }))
            return

        try:
            if participants_ids:
                await self.add_participants_to_chat(chat.id, participants_ids)
        except Exception as e:
            logger.error(f"Could not add participants to chat id {chat.id}: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Could not add participants to chat. Please try again later.'
            }))
            return

        chat_data = await self.serialize_chat(chat)
        message = CreateEmptyChatMessage(
            chat_id=chat_data['id'],
            participants=chat_data['participants'],
            created_at=chat_data['created_at'],
            updated_at=chat_data['updated_at'],
        )
        await self.send(text_data=json.dumps(message.to_dict()))

    async def handle_join_chat(self, data: dict[str, Any]) -> None:
        """
        Processes a request to join a chat and displays the latest message.
        """
        chat_id = data.get('chat_id')
        last_read_message_id = data.get('last_read_message', None)

        user = self.scope["user"]
        try:
            chat = await self.get_chat(chat_id=chat_id)
            if chat is None:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'The chat you are trying to join does not exist.'
                }))
                return

            is_participant = await self.is_user_in_chat(user=user, chat=chat)
            if is_participant:
                await self.send(text_data=json.dumps({
                    'type': 'info',
                    'message': 'You are already a participant in this chat.'
                }))
                return

            try:
                await self.add_participants_to_chat(chat_id=chat_id, participants_ids=[user.id])
            except Exception as e:
                logger.error(f"Failed to add user {user.id} to chat {chat_id}: {e}")
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Failed to join the chat. Please try again later.'
                }))
                return
            last_message_id = await self.get_last_message(chat_id=chat_id)
            message = JoinChatMessage(
                chat_id=chat_id,
                last_read_message=last_read_message_id or last_message_id,
                user=user
            )
            await self.send(text_data=json.dumps(message.to_dict()))


        except Exception as e:
            logger.error(f"Unexpected error when user {user.id} tried to join chat {chat_id}: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'An unexpected error occurred. Please try again later.'
            }))

    async def handle_create_new_message(self, data: dict[str, Any]) -> None:
        """
        Handles the creation of a new message in a chat.
        """
        from voicengerapp.serializers import WebSocketMessageSerializer
        chat_id = data.get('chat_id')
        text = data.get('text')

        user = self.scope['user']
        if not chat_id or not text:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid data. Chat ID and text are required.'
            }))
            return

        try:
            chat = await self.get_chat(chat_id=chat_id)
            if chat is None:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Chat not found.'
                }))
                return

            message = await self.create_message(chat_id=chat_id, text=text, sender=user)
            serializer = WebSocketMessageSerializer(message)
            serialized_data = serializer.data

            response_message = NewMessage(
                message_id=serialized_data['id'],
                chat_id=serialized_data['chat'],
                sender={
                    'id': serialized_data['sender']['id'],
                    'username': serialized_data['sender_username']
                },
                text=serialized_data['text'],
                timestamp=serialized_data['timestamp'],
                is_read=serialized_data['is_read']
            )

            await self.send(text_data=json.dumps(response_message.to_dict()))
        except Exception as e:
            logger.error(f"Error occurred while creating message in chat {chat_id}: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'An error occurred while creating the message. Please try again later.'
            }))

    @database_sync_to_async
    def get_all_chats(self):
        from voicengerapp.models import Chat
        return Chat.objects.all()

    @database_sync_to_async
    def serialize_chats(self, chats: list):
        from voicengerapp.serializers import ChatSerializer
        serializer = ChatSerializer(chats, many=True)
        return serializer.data

    @database_sync_to_async
    def serialize_chat(self, chat):
        from voicengerapp.serializers import ChatSerializer
        serializer = ChatSerializer(chat)
        return serializer.data

    @database_sync_to_async
    def serialize_message(self, message):
        from voicengerapp.serializers import MessageSerializer
        serializer = MessageSerializer(message)
        return serializer.data

    @database_sync_to_async
    def serialize_messages(self, messages):
        from voicengerapp.serializers import WebSocketMessageSerializer
        serializer = WebSocketMessageSerializer(messages, many=True)
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
    def get_last_message(self, chat_id: id):
        from voicengerapp.models import Message
        try:
            last_message = Message.objects.filter(chat_id=chat_id).latest('timestamp')
            return last_message.id
        except Message.DoesNotExist:
            return None

    @database_sync_to_async
    def get_messages(self, chat_id, date_from=None, date_to=None, last=None):
        from voicengerapp.models import Message
        messages = Message.objects.filter(chat_id=chat_id)

        if date_from:
            date_from = self.parse_custom_date(date_from)
            if date_from:
                messages = messages.filter(timestamp__date__gte=date_from)

        if date_to:
            date_to = parse_date(date_to)
            if date_to:
                messages = messages.filter(timestamp__date__lte=date_to)

        if last and str(last).isdigit():
            messages = messages.order_by('-timestamp')[:int(last)]

        return messages

    @database_sync_to_async
    def create_message(self, chat_id: int, text: str, sender):
        from voicengerapp.models import Message
        message = Message.objects.create(
            chat_id=chat_id,
            text=text,
            sender=sender,
            timestamp=timezone.now(),
            is_read=False
        )
        return message

    def parse_custom_date(self, date_str):
        if date_str == 'yesterday':
            return datetime.now().date() - timedelta(days=1)
        elif date_str == 'day_before_yesterday':
            return datetime.now().date() - timedelta(days=2)
        elif date_str == 'last_7_days':
            return datetime.now().date() - timedelta(days=7)
        else:
            return parse_date(date_str)
