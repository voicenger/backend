from channels.generic.websocket import AsyncWebsocketConsumer
import json
from voicengerapp.consumers.chat_commands import ChatCommands

import logging

logger = logging.getLogger('voicenger')

class ChatConsumer(AsyncWebsocketConsumer):
    """
    A WebSocket consumer for handling real-time chat interactions.

    This class manages the WebSocket connection, receives messages from the client,
    and delegates actions to the appropriate handlers in the `ChatCommands` class.

    Attributes:
        user (User): The user associated with the WebSocket connection. Initialized as None.
        commands (ChatCommands): Instance of `ChatCommands` used to handle various chat-related actions.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.commands = ChatCommands(self)

    async def connect(self):
        await self.accept()
        # user = self.scope.get('user')
        # if user and user.is_authenticated:
        #     self.user = user
        #     await self.accept()
        # else:
        #     await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            try:
                text_data_json = json.loads(text_data)
                message_type = text_data_json.get('type')
                data = text_data_json.get('data', {})

                if message_type == "getChats":
                    await self.commands.handle_get_chats()

                elif message_type == "getChatDetails":
                    await self.commands.handle_get_chat_detail(data)

                elif message_type == "createEmptyChat":
                    await self.commands.handle_create_empty_chat()

                elif message_type == "joinChat":
                    await self.commands.handle_join_chat(data, user=self.user)

                elif message_type == "newMessage":
                    await self.commands.handle_create_new_message(data, user=self.user)

                elif message_type == 'getChatMessages':
                    await self.commands.handle_get_chat_messages(data=data)

                else:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'Unknown message type'
                    }))

            except json.JSONDecodeError:
                logger.error('Invalid JSON received: %s', text_data)
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Invalid JSON'
                }))
            except Exception as e:
                logger.error('Error processing message: %s', str(e))
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'An unexpected error occurred'
                }))





