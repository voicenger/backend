from typing import Any, Optional
from voicengerapp.services.chat_service import ChatService
from voicengerapp.services.message_service import MessageService
import json

import logging

logger = logging.getLogger('voicenger')


class ChatCommands:
    """
    Handles various chat-related commands for a WebSocket consumer.

    Attributes:
        consumer: The WebSocket consumer that invokes the commands.
        chat_service: An instance of the `ChatService` for handling chat operations.
        message_service: An instance of the `MessageService` for handling message operations.
    """

    def __init__(self, consumer):
        self.consumer = consumer
        self.chat_service = ChatService()
        self.message_service = MessageService()

    async def get_chat_or_send_error(self, chat_id: int) -> Optional[dict]:
        """
        Retrieves a chat by its ID.

        This method fetches a chat from the chat service based on the provided chat ID.
        If the chat does not exist, it sends an error message and returns None.
        """
        chat = await self.chat_service.get_chat(chat_id)
        if chat is None:
            await self.consumer.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Chat not found.'
            }))
            return None
        return chat

    async def validate_chat_id(self, chat_id: Optional[int]) -> bool:
        """
        Validates the chat ID and sends an error message if it's missing.

        :param chat_id: The ID of the chat to validate.
        :return: True if chat ID is valid, otherwise False.
        """
        if chat_id is None:
            await self.consumer.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Chat ID is required.'
            }))
            return False
        return True

    async def handle_get_chats(self) -> None:
        """
        Handles a request to retrieve the list of chats.
        """
        try:
            chats = await self.chat_service.get_all_chats()
            serialized_chats = await self.chat_service.serialize_chats(chats)
            await self.consumer.send(text_data=json.dumps({
                'type': 'chatsList',
                'data': serialized_chats
            }))
        except Exception as e:
            logger.error(f"Error retrieving chats: {e}")
            await self.consumer.send(text_data=json.dumps({
                "type": "error",
                "message": "An error occurred while retrieving chats. Please try again later."
            }))

    async def handle_get_chat_detail(self, data: dict) -> None:
        """
        Handles a request to retrieve the details of a specific chat.
        """
        chat_id = data.get('chatId')

        if chat_id is None:
            await self.consumer.validate_chat_id()
            return

        chat = await self.get_chat_or_send_error(chat_id)
        if chat is None:
            return

        try:
            serialized_chat = await self.chat_service.serialize_chat(chat)
            await self.consumer.send(text_data=json.dumps({
                'type': 'chatDetails',
                'data': serialized_chat
            }))

        except Exception as e:
            logger.error(f"Error retrieving chat details for chat_id {chat_id}: {e}")
            await self.consumer.send(text_data=json.dumps({
                'type': 'error',
                'message': 'An error occurred while retrieving chat details. Please try again later.'
            }))

    async def handle_create_empty_chat(self) -> None:
        """
        Handles the creation of a new chat.

        This method processes incoming data to create a new chat and optionally add participants to it.
        """
        try:
            chat = await self.chat_service.create_chat()
        except Exception as e:
            logger.error(f"Could not create chat: {e}")
            await self.consumer.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Could not create chat. Please try again later.'
            }))
            return

        chat_data = await self.chat_service.serialize_chat(chat)
        await self.consumer.send(text_data=json.dumps({
            'type': "emptyChatCreated",
            'data': {
                'id': chat_data['id'],
                'created_at': chat_data['created_at'],
                'updated_at': chat_data['updated_at'],
            }
        }))

    async def handle_join_chat(self, data: dict[str, Any], user) -> None:
        """
        Processes a request to join a chat and displays the latest message.
        """
        chat_id = data.get('chat')
        last_read_message_id = data.get('last_read_message', None)

        if chat_id is None:
            await self.consumer.validate_chat_id()
            return

        chat = await self.get_chat_or_send_error(chat_id)
        if chat is None:
            return

        try:
            is_participant = await self.chat_service.is_user_in_chat(user=user, chat=chat)
            if is_participant:
                await self.consumer.send(text_data=json.dumps({
                    'type': 'info',
                    'message': 'You are already a participant in this chat.'
                }))
                return

            await self.chat_service.add_participants_to_chat(chat_id=chat_id, participants_ids=[user.id])
            last_message_id = await self.message_service.get_last_message(chat_id=chat_id)

            message_data = {
                "chat": chat_id,
                "user": {
                    "id": user.id,
                    "username": user.username
                }
            }
            if last_read_message_id or last_message_id:
                message_data["last_read_message"] = last_read_message_id or last_message_id

            await self.consumer.send(text_data=json.dumps({
                'type': 'chatJoined',
                'data': message_data
            }))

        except Exception as e:
            logger.error(f"Unexpected error when user {user.id} tried to join chat {chat_id}: {e}")
            await self.consumer.send(text_data=json.dumps({
                'type': 'error',
                'message': 'An unexpected error occurred. Please try again later.'
            }))

    async def handle_create_new_message(self, data: dict[str, Any], user) -> None:
        """
        Handles the creation of a new message in a chat.
        """
        from voicengerapp.serializers import WebSocketMessageSerializer

        chat_id = data.get('chat')
        text = data.get('text')
        is_read = data.get('is_read', False)

        if not chat_id or not text:
            await self.consumer.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid data. Chat ID and text are required.'
            }))
            return
        chat = await self.get_chat_or_send_error(chat_id)
        if chat is None:
            return

        try:
            message = await (self.message_service.create_message(
                chat_id=chat_id,
                text=text,
                sender=user,
                is_read=is_read
            ))
            serializer = WebSocketMessageSerializer(message)
            serialized_data = serializer.data

            await self.consumer.send(text_data=json.dumps({
                'type': 'messageCreated',
                'data': {
                    'id': serialized_data['id'],
                    'chat': serialized_data['chat'],
                    'sender': {
                        'id': serialized_data['sender']['id'],
                        'username': serialized_data['sender_username']
                    },
                    'text': serialized_data['text'],
                    'timestamp': serialized_data['timestamp'],
                    'is_read': serialized_data['is_read']
                }
            }))

        except Exception as e:
            logger.error(f"Error occurred while creating message in chat {chat_id}: {e}")
            await self.consumer.send(text_data=json.dumps({
                'type': 'error',
                'message': 'An error occurred while creating the message. Please try again later.'
            }))


    async def handle_get_chat_messages(self, data: dict[str, Any]) -> None:
        """
        Handles the retrieval of messages from a chat with optional filtering by date and/or limit.
        """
        chat_id = data.get('chatId')
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        last = data.get('last')

        if chat_id is None:
            await self.consumer.validate_chat_id()
            return

        chat = await self.get_chat_or_send_error(chat_id)
        if chat is None:
            return

        try:
            messages = await self.message_service.get_messages(chat_id, date_from, date_to, last)
            serialized_messages = await self.message_service.serialize_messages(messages)
            await self.consumer.send(text_data=json.dumps({
                'type': 'chatMessages',
                'data': serialized_messages
            }))
        except Exception as e:
            logger.error(f"Error handling chat messages for chat_id {chat_id}: {e}")
            await self.consumer.send(text_data=json.dumps({
                'type': 'error',
                'message': 'An error occurred while retrieving messages. Please try again later.'
            }))
