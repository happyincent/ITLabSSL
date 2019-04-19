import pickle
import datetime

from django.utils import timezone
from django.conf import settings

from django.core.cache import cache
from home.models import Device

from channels.generic.websocket import AsyncJsonWebsocketConsumer

class StarConsumer(AsyncJsonWebsocketConsumer):
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

            if content['cmd'] == 'update_info':            
                ts = datetime.datetime.now(datetime.timezone.utc)
                ts = timezone.localtime(ts)
                content['data']['timestamp'] = ts.strftime(settings.INFO_TIMESTR)
                cache.set('{}{}'.format(self.device_id, settings.INFO_POSTFIX), pickle.dumps(content['data']), settings.INFO_TIMEOUT)

            if content['cmd'] in ['update_info']:
                await self.channel_layer.group_send(
                    self.device_id,
                    {
                        'type': 'broatcast_json',
                        'content': content
                    }
                )
        
        else:
            await self.close()
    
    async def broatcast_json(self, event):
        await self.send_json(event['content'])