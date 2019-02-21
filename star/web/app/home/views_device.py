import uuid

from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from .views_decorator import *

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers

from django.contrib.auth.models import User
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

    def form_valid(self, form):
        if not User.objects.filter(username=form.instance.name).exists():
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        
        return HttpResponseRedirect(reverse('device_edit_fail', kwargs={'pk': form.instance.name}))
        
    def get_success_url(self):
        User.objects.create_user(
            username=self.object.name,
            email='{}@itlab.ee.ncku.edu.tw'.format(self.object.name),
            password=str(self.object.token)
        )
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
    
    def form_valid(self, form):
        if not User.objects.filter(username=form.instance.name).exists():
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        
        return HttpResponseRedirect(reverse('device_edit_fail', kwargs={'pk': form.instance.name}))
        
    def get_success_url(self):
        User.objects.filter(username=self.object.name).delete()
        return reverse('device_list')

@method_decorator(legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class ResetToken(View):

    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):
        print(kwargs['pk'])
        
        if not (Device.objects.filter(name=kwargs['pk']).exists() and 
                User.objects.filter(username=kwargs['pk']).exists()):
            raise Http404('Page Not Found')
        
        new_token = uuid.uuid4()
        Device.objects.filter(name=kwargs['pk']).update(token=new_token)
        user = User.objects.filter(username=kwargs['pk']).first()
        user.set_password(str(new_token))
        user.save()

        return HttpResponseRedirect(reverse('device_update', kwargs={'pk': kwargs['pk']}))

@method_decorator(legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceEditFail(TemplateView):
    template_name = 'home/device_err.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_name'] = kwargs['pk']
        return context