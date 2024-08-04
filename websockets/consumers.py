import json
from asyncio.log import logger
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from voicengerdb.models import Message, Chat, User, ChatParticipant, MessageReadReceipt

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        #Log event
        logger.debug(f"User connected to chat: {self.room_name}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.send_message_history()

    async def disconnect(self, close_code):
        #Log event
        logger.debug(f"User disconnected from chat: {self.room_name} with code {close_code}")

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = self.scope['user'].id

        #Log receive message
        logger.debug(f"Message received in chat {self.room_name} : {message}")

        #Save message
        await self.save_message(user_id, self.room_name, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id
            }
        )

        #Mark message receive
        await self.mark_messages_as_read(user_id, self.room_name)

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']

        #Log send message
        logger.debug(f"Message sent to chat {self.room_name} from user {user_id}: {message}")

        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id
        }))

    @database_sync_to_async
    def save_message(self, user_id, room_name, message):
        user = User.objects.get(id=user_id)
        chat = Chat.objects.get(id=room_name)  # Предполагается, что room_name соответствует идентификатору чата
        Message.objects.create(user=user, chat=chat, content=message, message_type=Message.TEXT)

    @database_sync_to_async
    def get_chat_history(self, room_name):
        return Message.objects.filter(chat__id=room_name).order_by('sent_at')

    @database_sync_to_async
    def mark_messages_as_read(self, user_id, room_name):
        chat_participant = ChatParticipant.objects.get(user_id=user_id, chat__id=room_name)
        unread_messages = Message.objects.filter(chat__id=room_name).exclude(
            messagereadreceipt__chat_participant=chat_participant)
        MessageReadReceipt.objects.bulk_create([
            MessageReadReceipt(message=message, chat_participant=chat_participant) for message in unread_messages
        ])

    async def send_message_history(self):
        messages = await self.get_chat_history(self.room_name)
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message.content,
                'user_id': message.user.id,
                'sent_at': message.sent_at.isoformat(),
            }))

