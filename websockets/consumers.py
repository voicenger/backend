import json
from channels.generic.websocket import AsyncWebsocketConsumer

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'your_group'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        print("WebSocket connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("WebSocket disconnected")

    async def receive(self, text_data):
        if not text_data:
            print("Received empty message")
            await self.send(text_data=json.dumps({
                'error': 'Empty message'
            }))
            return

        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            print(f"Message received: {message}")

            response = await self.call_backend_method(message)
            await self.send(text_data=json.dumps({
                'response': response
            }))
        except json.JSONDecodeError:
            print("Received invalid JSON")
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))

    async def call_backend_method(self, message):
        result = await self.some_backend_function(message)
        return result

    async def some_backend_function(self, message):
        return {"status": "success", "data": message}
