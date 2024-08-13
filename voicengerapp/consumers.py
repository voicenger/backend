import json

import httpx
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings


class Token(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        request = json.loads(text_data)

        method = request.get('method', 'GET')
        url = request.get('url')
        headers = request.get('headers', {})
        data = request.get('data', None)

        # Формирование полного URL
        full_url = f'{settings.API_BASE_URL}{url}'

        # Ограничение на метод POST
        if method != 'POST':
            response_data = {
                "error": "Only POST method is allowed for this endpoint"
            }
            await self._send_response(response_data)
            return

        async with httpx.AsyncClient() as client:
            response = await client.post(full_url, json=data, headers=headers)

            response_data = {
                "status_code": response.status_code,
                "data": response.json()
            } if response else {
                "error": "Failed to perform the request"
            }

            await self._send_response(response_data)

    async def _send_response(self, data):
        await self.send(text_data=json.dumps(data))
