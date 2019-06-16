import pickle

from django.utils import timezone
from django.conf import settings

from django.core.cache import cache
from home.models import Device

from channels.generic.websocket import AsyncJsonWebsocketConsumer

class StarConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.client_type = self.scope['url_route']['kwargs']['client_type']
        self.device_id = self.scope['url_route']['kwargs']['device_id']
                
        # check device exist
        if cache.get(self.device_id) != None:

            # /ws/edge
            if self.client_type == 'edge' and self.scope['token'] == cache.get(self.device_id):
                cache.set('{}{}'.format(self.device_id, settings.CHANNEL_POSTFIX), self.channel_name, timeout=None)
                await self.accept()

            # /ws/browser
            elif self.client_type == 'browser' and self.scope['user'].is_authenticated:
                await self.channel_layer.group_add(
                    self.device_id,
                    self.channel_name
                )
                await self.accept()
            
            else:
                await self.close()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.client_type == 'edge':
            cache.delete('{}{}'.format(self.device_id, settings.CHANNEL_POSTFIX))
            await self.channel_layer.group_send(
                self.device_id, 
                {'type': 'broatcast_json', 'content': {'cmd': 'error', 'data': 'Edge Device is disconnected.'}}
            )

        elif self.client_type == 'browser':
            await self.channel_layer.group_discard(
                self.device_id,
                self.channel_name
            )

    async def receive_json(self, content):

        # /ws/edge (check token for each request)
        if content['cmd'] == 'update_info' and (
            self.client_type == 'edge' and self.scope['token'] == cache.get(self.device_id)
        ):
            now = timezone.localtime(timezone.now())
            content['data']['timestamp'] = now.strftime(settings.INFO_TIMESTR)

            await self.channel_layer.group_send(
                self.device_id, 
                {'type': 'broatcast_json', 'content': content}
            )

            cache.set('{}{}'.format(self.device_id, settings.INFO_POSTFIX), pickle.dumps(content['data']), settings.INFO_TIMEOUT)

        # /ws/browser (check user for each request)
        elif content['cmd'] in ['led_ctrl', 'pir_ctrl', 'update_pir_millis'] and (
            self.client_type == 'browser' and self.scope['user'].is_authenticated and self.scope['user'].is_staff
        ):
            if cache.get('{}{}'.format(self.device_id, settings.CHANNEL_POSTFIX)) != None:
                await self.channel_layer.send(
                    cache.get('{}{}'.format(self.device_id, settings.CHANNEL_POSTFIX)),
                    {'type': 'unicast_json', 'content': content}
                )
            else:
                await self.channel_layer.send(
                    self.channel_name,
                    {'type': 'unicast_json', 'content': {'cmd': 'error', 'data': 'Edge Device is disconnected.'}}
                )
        
        else:
            await self.close()
    
    async def unicast_json(self, event):
        await self.send_json(event['content'])

    async def broatcast_json(self, event):
        await self.send_json(event['content'])