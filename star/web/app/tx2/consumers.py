from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .models import DeviceInfoNow

class InfoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_name = self.scope['url_route']['kwargs']['device_name']
        
        print(self.channel_name, '~~', self.device_name)

        await self.channel_layer.group_add(
            self.device_name,
            self.channel_name
        )

        await self.accept() if self.scope['user'].is_authenticated else self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.device_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.device_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))