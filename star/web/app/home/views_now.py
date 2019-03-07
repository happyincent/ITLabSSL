from django.views.generic import TemplateView
from .views_decorator import *

from django.http import Http404
from django.conf import settings

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
        context['device_info'] = Device.objects.get(pk=kwargs['pk']).info_history.order_by('-timestamp').first()
        return context