import pickle

from django.views.generic import TemplateView
from .views_decorator import *

from django.http import Http404
from django.conf import settings

from django.core.cache import cache
from .models import Device

@method_decorator(legal_user, name='dispatch')
class DeviceInfo(TemplateView):
    template_name = 'home/device_info_now.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if not Device.objects.filter(pk=kwargs['pk']).exists():
            raise Http404
        
        context['device_name'] = kwargs['pk']
        context['hls_url'] = settings.HLS_URL
        
        info_now = cache.get('{}{}'.format(kwargs['pk'], settings.INFO_POSTFIX))
        context['device_info'] = None if info_now==None else pickle.loads()
        
        return context