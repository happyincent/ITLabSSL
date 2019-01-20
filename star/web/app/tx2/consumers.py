from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
import datetime

from channels.db import database_sync_to_async
from home.models import Device
from .models import DeviceInfoNow

class InfoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.device_name = self.scope['url_route']['kwargs']['device_name']

        await self.channel_layer.group_add(
            self.device_name,
            self.channel_name
        )

        # await self.accept()

        if self.scope['user'].is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.device_name,
            self.channel_name
        )

    async def receive_json(self, content):
        await self.updateDB(content)

        await self.channel_layer.group_send(
            self.device_name,
            {
                'type': 'send_info',
                'content': content
            }
        )
    
    async def send_info(self, event):
        content = event['content']

        await self.send_json({
            'temperature': content.get('temperature', None),
            'humidity': content.get('humidity', None),
            'pm2_5': content.get('pm2_5', None),
            'loudness': content.get('loudness', None),
            'light_intensity': content.get('light_intensity', None),
            'uv_intensity': content.get('uv_intensity', None),
            'ir_sensed': content.get('ir_sensed', None),
            'timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            # 'timestamp': datetime.datetime.utcnow().strftime('%s'),
        })

    @database_sync_to_async
    def updateDB(self, content):
        device = Device.objects.filter(pk=self.device_name).first()
        if device == None:
            return

        DeviceInfoNow.objects.update_or_create(
            device = device,
            defaults = {
                'temperature': content.get('temperature', None),
                'humidity': content.get('humidity', None),
                'pm2_5': content.get('pm2_5', None),
                'loudness': content.get('loudness', None),
                'light_intensity': content.get('light_intensity', None),
                'uv_intensity': content.get('uv_intensity', None),
                'ir_sensed': content.get('ir_sensed', None),
            }
        )