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
            print(f"Received message: {text_data}")
            text_data_json = json.loads(text_data)
            print(f"Decoded JSON: {text_data_json}")

            api_endpoint = text_data_json.get('api_endpoint')
            if not api_endpoint:
                print("API endpoint is missing")
                await self.send(text_data=json.dumps({
                    'error': 'API endpoint is missing'
                }))
                return

            request_data = text_data_json.get('data', {})
            method = text_data_json.get('method', 'POST').upper()
            headers = text_data_json.get('headers', {})

            print(f"API endpoint received: {api_endpoint}")
            print(f"Request data: {request_data}")
            print(f"Request method: {method}")
            print(f"Request headers: {headers}")

            response = await self.call_api(api_endpoint, request_data, method, headers)
            print(f"API response: {response}")

            await self.send(text_data=json.dumps({
                'response': response
            }))
        except json.JSONDecodeError:
            print("Received invalid JSON")
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            await self.send(text_data=json.dumps({
                'error': 'An unexpected error occurred',
                'message': str(e)
            }))

    async def call_api(self, endpoint, data, method, headers):
        async with httpx.AsyncClient() as client:
            try:
                if method == 'GET':
                    response = await client.get(endpoint, params=data, headers=headers)
                elif method == 'POST':
                    response = await client.post(endpoint, json=data, headers=headers)
                elif method == 'PUT':
                    response = await client.put(endpoint, json=data, headers=headers)
                elif method == 'PATCH':
                    response = await client.patch(endpoint, json=data, headers=headers)
                elif method == 'DELETE':
                    response = await client.delete(endpoint, headers=headers)
                else:
                    return {"status": "error", "message": f"Unsupported method {method}"}

                response.raise_for_status()
                response_data = response.json() if response.content else {}
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
