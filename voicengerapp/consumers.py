import json

from channels.generic.websocket import AsyncWebsocketConsumer

MESSAGE_CREATION_COMMAND = 'create_message'
USER_INFO_COMMAND = 'get_user'
MESSAGE_CREATED_RESPONSE = 'message_created'
USER_INFO_RESPONSE = 'user_info'
DATA_KEY = 'data'


class UserMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('type')

        if command == MESSAGE_CREATION_COMMAND:
            await self.create_message(data[DATA_KEY])
        elif command == USER_INFO_COMMAND:
            await self.get_user_info(data[DATA_KEY])

    async def create_message(self, data):
        message = self.generate_response(data, ['message_id', 'chat_id', 'text', 'timestamp'])
        await self._send_response(MESSAGE_CREATED_RESPONSE, message)

    async def get_user_info(self, data):
        user_info = self.generate_response(data, ['user_id', 'username', 'email'])
        await self._send_response(USER_INFO_RESPONSE, user_info)

    def generate_response(self, data, keys):
        return {key: data.get(key, '') for key in keys}

    async def _send_response(self, type_, data):
        await self.send(text_data=json.dumps({
            'type': type_,
            'data': data
        }))
