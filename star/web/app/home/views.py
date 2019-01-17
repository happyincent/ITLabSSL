import os
from django.http import HttpResponse, Http404, JsonResponse
from django.core import serializers
from django.urls import reverse, reverse_lazy

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import TemplateView

from allauth.account.decorators import verified_email_required
from revproxy.views import ProxyView

from .models import Device

@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'home/home.html'

@method_decorator(login_required, name='dispatch')
@method_decorator(verified_email_required, name='dispatch')
class Aboutus(TemplateView):
    template_name = 'home/aboutus.html'

###

@method_decorator(login_required, name='dispatch')
@method_decorator(verified_email_required, name='dispatch')
class DeviceList(TemplateView):
    template_name = 'home/device_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = Device.objects.all()
        context['devices_json'] = serializers.serialize("json", context['devices'])
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(verified_email_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceCreate(CreateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = '__all__'

    def get_success_url(self):
        print(self.object.name)
        return reverse('device_list')

@method_decorator(login_required, name='dispatch')
@method_decorator(verified_email_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = ['longitude', 'latitude', 'uri']
    
    def get_success_url(self):
        print(self.object.name)
        return reverse('device_list')

@method_decorator(login_required, name='dispatch')
@method_decorator(verified_email_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'home/delete_device.html'
    success_url = reverse_lazy('device_list')

###

@method_decorator(login_required, name='dispatch')
@method_decorator(verified_email_required, name='dispatch')
class DeviceInfoNow(TemplateView):
    template_name = 'home/device_info_now.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device_name = kwargs['device_name']
        
        if not Device.objects.filter(name=device_name).exists():
            raise Http404('Page Not Found')
        
        context['device_name'] = device_name
        context['message'] = 'test'
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(verified_email_required, name='dispatch')
class DeviceInfoHistory(TemplateView):
    template_name = 'home/device_info_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_name'] = kwargs['device_name']
        return context

###



###

HLS_KEY_DIR = '/tmp/key'

@login_required
@verified_email_required
def key(request, stream):
    file_path = os.path.join(HLS_KEY_DIR, stream)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/octet-stream')
    raise Http404

@method_decorator(login_required, name='dispatch')
@method_decorator(verified_email_required, name='dispatch')
class Vod(ProxyView):
    upstream = 'http://nginx:62401/record/'
