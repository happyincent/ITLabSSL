import urllib.parse

from django.views.generic import TemplateView
from .views_decorator import *

from django.http import Http404
from django.conf import settings

from .models import Device

@method_decorator(legal_user, name='dispatch')
class DeviceInfoHistory(TemplateView):
    template_name = 'home/device_info_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not Device.objects.filter(pk=kwargs.get('pk')).exists():
            raise Http404
        
        context['vod_url'] = urllib.parse.urljoin(settings.VOD_URL, '{}/'.format(kwargs.get('pk')))
        return context