import pickle
import datetime

from django.utils import timezone
from django.conf import settings

from django.core.cache import cache
from home.models import Device

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
            
            ts = datetime.datetime.now(datetime.timezone.utc)
            ts = timezone.localtime(ts)
            content['timestamp'] = ts.strftime(settings.INFO_TIMESTR)

            await self.channel_layer.group_send(
                self.device_name,
                {
                    'type': 'send_info',
                    'content': content
                }
            )

            cache.set('{}{}'.format(self.device_name, settings.INFO_POSTFIX), pickle.dumps(content), settings.INFO_TIMEOUT)
        else:
            await self.close()
    
    async def send_info(self, event):
        await self.send_json(event['content'])