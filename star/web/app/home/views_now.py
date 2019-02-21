import os

from django.views.generic import TemplateView
from .views_decorator import *

from django.http import HttpResponse, Http404

from .models import Device

HLS_KEY_DIR = '/tmp/key'

@method_decorator(legal_user, name='dispatch')
class DeviceInfo(TemplateView):
    template_name = 'home/device_info_now.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if not Device.objects.filter(pk=kwargs['pk']).exists():
            raise Http404('Page Not Found')
        
        context['device_name'] = kwargs['pk']
        context['device_info'] = Device.objects.get(pk=kwargs['pk']).info_now.first()
        return context

@login_required
@verified_email_required
def key(request, path):
    file_path = os.path.join(HLS_KEY_DIR, path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/octet-stream')
    
    raise Http404