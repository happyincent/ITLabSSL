import json
import datetime

from django.utils import timezone
from django.core.cache import cache

from channels.db import database_sync_to_async
from home.models import Device
from .models import InstantInfo

from channels.generic.websocket import AsyncJsonWebsocketConsumer

class InfoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.device_name = self.scope['url_route']['kwargs']['device_name']

        await self.channel_layer.group_add(
            self.device_name,
            self.channel_name
        )
        
        self.is_token_valid = self.scope['token'] != None and self.scope['token'] == cache.get(self.device_name)

        if self.is_token_valid or self.scope['user'].is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.device_name,
            self.channel_name
        )

    async def receive_json(self, content):
        if self.is_token_valid:
            await self.updateDB(content)

            await self.channel_layer.group_send(
                self.device_name,
                {
                    'type': 'send_info',
                    'content': content
                }
            )
        else:
            await self.close()
    
    async def send_info(self, event):
        content = event['content']

        ts = datetime.datetime.now(datetime.timezone.utc)
        ts = timezone.localtime(ts)

        await self.send_json({
            'temperature': content.get('temperature', None),
            'humidity': content.get('humidity', None),
            'pm2_5': content.get('pm2_5', None),
            'loudness': content.get('loudness', None),
            'light_intensity': content.get('light_intensity', None),
            'uv_intensity': content.get('uv_intensity', None),
            'ir_sensed': content.get('ir_sensed', None),
            'timestamp': ts.strftime('%Y-%m-%d %H:%M:%S %z'),
        })

    @database_sync_to_async
    def updateDB(self, content):
        device = Device.objects.filter(pk=self.device_name).first()
        if device == None:
            return

        InstantInfo.objects.update_or_create(
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