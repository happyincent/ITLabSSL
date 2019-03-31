import pickle
import datetime

from django.utils import timezone
from django.conf import settings

from django.core.cache import cache
from home.models import Device

from channels.generic.websocket import AsyncJsonWebsocketConsumer

class InfoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        
        if cache.get(self.device_id) != None:
            await self.channel_layer.group_add(
                self.device_id,
                self.channel_name
            )

            if self.scope['user'].is_authenticated or self.scope['token'] == cache.get(self.device_id):
                await self.accept()
                return
        
        await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.device_id,
            self.channel_name
        )

    async def receive_json(self, content):
        # check if reset or delete token
        if self.scope['token'] == cache.get(self.device_id):
            
            ts = datetime.datetime.now(datetime.timezone.utc)
            ts = timezone.localtime(ts)
            content['timestamp'] = ts.strftime(settings.INFO_TIMESTR)

            await self.channel_layer.group_send(
                self.device_id,
                {
                    'type': 'send_info',
                    'content': content
                }
            )

            cache.set('{}{}'.format(self.device_id, settings.INFO_POSTFIX), pickle.dumps(content), settings.INFO_TIMEOUT)
        else:
            await self.close()
    
    async def send_info(self, event):
        await self.send_json(event['content'])