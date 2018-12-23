import os
from django.http import HttpResponse, Http404

from django.views.generic import TemplateView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required

from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from .models import Device

@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'home/home.html'

###

@method_decorator(login_required, name='dispatch')
@method_decorator(verified_email_required, name='dispatch')
class DeviceList(TemplateView):
    template_name = 'home/device_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = Device.objects.all()
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
class DeviceInfo(TemplateView):
    template_name = 'home/device_info.html'

###

HLS_KEY_DIR = '/tmp/key'

@login_required
def key(request, stream):
    file_path = os.path.join(HLS_KEY_DIR, stream)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/octet-stream')
    raise Http404