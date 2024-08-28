from channels.generic.websocket import AsyncWebsocketConsumer
import json
from voicengerapp.consumers.chat_commands import ChatCommands
from django.conf import settings
from jose import JWTError
import logging
from channels.db import database_sync_to_async

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
        try:
            token = self.scope['query_string'].decode('utf8').split('=')[1]
            self.user = await self.get_user_from_token(token)
            if self.user:
                await self.accept()
            else:
                await self.close(code=4001)  # Custom close code for unauthorized access
        except (JWTError, IndexError, ValueError) as e:
            logger.error(f"WebSocket connection error: {str(e)}")
            await self.close()

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
    @database_sync_to_async
    def get_user_from_token(self, token):
        from voicengerapp.models import User
        from voicengerapp.utils import decode_and_verify_token
        try:
            user_data = decode_and_verify_token(token)
            logger.debug(f"Decoded token data: {user_data}")

            # Use the 'sub' field to find the user. 'sub' give from auth0
            user_id = user_data.get('sub')
            if user_id:
                # Assuming you have a method to find a user by 'sub'
                user = User.objects.get(auth0_sub=user_id)  # Or another suitable method for lookup
                return user
            else:
                logger.error("User ID not found in token data")
                return None
        except ValueError as e:
            logger.error(f"Token validation error: {e}")
            return None
        except User.DoesNotExist:
            logger.error("User does not exist")
            return None