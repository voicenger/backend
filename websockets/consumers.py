import json
from asyncio.log import logger
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from voicengerdb.models import Message, Chat, User, ChatParticipant, MessageReadReceipt
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Log the connection event
        logger.debug("User connected")

        # Accept the WebSocket connection
        await self.accept()

        # Set user status to online
        await self.update_user_status(True)

    async def disconnect(self, close_code):
        # Log the disconnection event
        logger.debug(f"User disconnected with code {close_code}")

        # Set user status to offline
        await self.update_user_status(False)

    async def receive(self, text_data):
        # Decode the received data
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')  # Extract action from message
        room_name = text_data_json.get('room_name')  # Extract room_name from message if applicable
        message_type = text_data_json.get('message_type', Message.TEXT)
        user_id = self.scope['user'].id

        # Log the received message
        logger.debug(f"Message received: {text_data_json}")

        # Process different actions
        if action == 'send_message':
            if message_type == Message.TEXT:
                message_content = text_data_json.get('message')
                await self.save_message(user_id, room_name, message_content, message_type)
            elif message_type == Message.AUDIO:
                audio_file = text_data_json.get('audio_file')
                await self.save_message(user_id, room_name, None, message_type, audio_file=audio_file)
            elif message_type == Message.VIDEO:
                video_file = text_data_json.get('video_file')
                await self.save_message(user_id, room_name, None, message_type, video_file=video_file)
            elif message_type == Message.IMAGE:
                image_file = text_data_json.get('image_file')
                await self.save_message(user_id, room_name, None, message_type, image_file=image_file)
            elif message_type == Message.FILE:
                attached_file = text_data_json.get('attached_file')
                await self.save_message(user_id, room_name, None, message_type, attached_file=attached_file)

            # Send the message to all participants in the room
            await self.channel_layer.group_send(
                f'chat_{room_name}',
                {
                    'type': 'chat_message',
                    'message': text_data_json,
                    'user_id': user_id
                }
            )

            # Mark messages as read
            await self.mark_messages_as_read(user_id, room_name)
        elif action == 'get_history':
            # Send message history
            await self.send_message_history(room_name)

    async def chat_message(self, event):
        # Get the message and user ID from the event
        message = event['message']
        user_id = event['user_id']

        # Log the sent message
        logger.debug(f"Message sent from user {user_id}: {message}")

        # Send the message to the client
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id
        }))

    @database_sync_to_async
    def save_message(self, user_id, room_name, content, message_type, audio_file=None, video_file=None, image_file=None, attached_file=None):
        # Get the user and chat objects
        user = User.objects.get(id=user_id)
        chat = Chat.objects.get(id=room_name)  # Assuming room_name corresponds to the chat ID

        # Save the message to the database based on its type
        if message_type == Message.TEXT:
            Message.objects.create(user=user, chat=chat, content=content, message_type=message_type)
        elif message_type == Message.AUDIO:
            Message.objects.create(user=user, chat=chat, audio_file=audio_file, message_type=message_type)
        elif message_type == Message.VIDEO:
            Message.objects.create(user=user, chat=chat, video_file=video_file, message_type=message_type)
        elif message_type == Message.IMAGE:
            Message.objects.create(user=user, chat=chat, image_file=image_file, message_type=message_type)
        elif message_type == Message.FILE:
            Message.objects.create(user=user, chat=chat, attached_file=attached_file, message_type=message_type)

    @database_sync_to_async
    def get_chat_history(self, room_name):
        # Retrieve the message history for the room
        return Message.objects.filter(chat__id=room_name).order_by('sent_at')

    @database_sync_to_async
    def mark_messages_as_read(self, user_id, room_name):
        # Get the chat participant object
        chat_participant = ChatParticipant.objects.get(user_id=user_id, chat__id=room_name)
        # Find unread messages
        unread_messages = Message.objects.filter(chat__id=room_name).exclude(
            messagereadreceipt__chat_participant=chat_participant)
        # Create read receipt entries for unread messages
        MessageReadReceipt.objects.bulk_create([
            MessageReadReceipt(message=message, chat_participant=chat_participant) for message in unread_messages
        ])

    async def send_message_history(self, room_name):
        # Retrieve the message history for the room
        messages = await self.get_chat_history(room_name)
        # Send the message history to the client
        for message in messages:
            message_data = {
                'message': message.content,
                'user_id': message.user.id,
                'sent_at': message.sent_at.isoformat(),
                'message_type': message.message_type,
            }
            # Add the appropriate file URL if the message is not text
            if message.message_type == Message.AUDIO:
                message_data['audio_file'] = message.audio_file.url
            elif message.message_type == Message.VIDEO:
                message_data['video_file'] = message.video_file.url
            elif message.message_type == Message.IMAGE:
                message_data['image_file'] = message.image_file.url
            elif message.message_type == Message.FILE:
                message_data['attached_file'] = message.attached_file.url

            await self.send(text_data=json.dumps(message_data))

    @database_sync_to_async
    def update_user_status(self, is_online):
        # Update the user's online status
        user = User.objects.get(id=self.scope['user'].id)
        user.is_online = is_online
        user.last_login_at = timezone.now() if is_online else user.last_login_at
        user.save()
