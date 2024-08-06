import json
import httpx
from channels.generic.websocket import AsyncWebsocketConsumer

class APIGatewayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connected")

    async def disconnect(self, close_code):
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
            api_endpoint = text_data_json['api_endpoint']
            request_data = text_data_json.get('data', {})
            method = text_data_json.get('method', 'POST').upper()

            print(f"API endpoint received: {api_endpoint}")

            response = await self.call_api(api_endpoint, request_data, method)
            await self.send(text_data=json.dumps({
                'response': response
            }))
        except json.JSONDecodeError:
            print("Received invalid JSON")
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))

    async def call_api(self, endpoint, data, method):
        async with httpx.AsyncClient() as client:
            try:
                if method == 'GET':
                    response = await client.get(endpoint, params=data)
                elif method == 'POST':
                    response = await client.post(endpoint, json=data)
                elif method == 'PUT':
                    response = await client.put(endpoint, json=data)
                elif method == 'PATCH':
                    response = await client.patch(endpoint, json=data)
                elif method == 'DELETE':
                    response = await client.delete(endpoint, json=data)
                else:
                    return {"status": "error", "message": f"Unsupported method {method}"}

                response_data = response.json()
                return {"status": "success", "data": response_data}
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}")
                return {"status": "error", "message": str(e)}
            except Exception as e:
                print(f"An error occurred: {e}")
                return {"status": "error", "message": "An internal error occurred"}

# Пример JSON-запроса через WebSocket
# {
#   "api_endpoint": "http://127.0.0.1:8000/api/group_chats/",
#   "data": {
#     "name": "New Group Chat"
#   },
#   "method": "POST"
# }
