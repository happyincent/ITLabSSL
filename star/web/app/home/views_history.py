import os
import uuid
import urllib.parse

from django.views.generic import TemplateView
from .views_decorator import *

from django.http import Http404
from django.core.cache import cache
from django.conf import settings

from .models import Device

@method_decorator(legal_user, name='dispatch')
class DeviceInfoHistory(TemplateView):
    template_name = 'home/device_info_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not Device.objects.filter(pk=kwargs.get('pk')).exists():
            raise Http404

        token = cache.get(self.request.user)
        if token == None:
            token = uuid.uuid4()
            cache.set(self.request.user, str(token), settings.APIToken_TIMEOUT)
        
        context['device_id'] = kwargs.get('pk')
        context['vod_url'] = urllib.parse.urljoin(settings.VOD_URL, '{}/'.format(kwargs.get('pk')))
        context['api_token'] = token
        return context