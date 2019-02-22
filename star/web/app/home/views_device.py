import uuid

from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from .views_decorator import *

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.core.cache import cache

from .models import Device

@method_decorator(legal_user, name='dispatch')
class DeviceList(TemplateView):
    template_name = 'home/device_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = Device.objects.all()
        context['devices_json'] = serializers.serialize("json", context['devices'])
        return context  

@method_decorator(legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceCreate(CreateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = ['name', 'longitude', 'latitude', 'ssh_pub']
        
    def get_success_url(self):
        cache.set(self.object.name, str(self.object.token), timeout=None)
        return reverse('device_update', kwargs={'pk': self.object.name})

@method_decorator(legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = ['longitude', 'latitude', 'ssh_pub']
    
    def get_success_url(self):
        return reverse('device_list')

@method_decorator(legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'home/delete_device.html'
        
    def get_success_url(self):
        cache.delete(self.object.name)
        return reverse('device_list')

@method_decorator(legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class ResetToken(View):

    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):        
        if not Device.objects.filter(name=kwargs['pk']).exists():
            raise Http404('Page Not Found')
        
        new_token = uuid.uuid4()
        Device.objects.filter(name=kwargs['pk']).update(token=new_token)
        cache.set(kwargs['pk'], str(new_token), timeout=None)

        return HttpResponseRedirect(reverse('device_update', kwargs={'pk': kwargs['pk']}))