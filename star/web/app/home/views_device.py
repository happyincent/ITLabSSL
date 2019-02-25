import uuid
import subprocess
from sshpubkeys import SSHKey, AuthorizedKeysFile

from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from .views_decorator import *

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.core.cache import cache
from django.conf import settings

from .models import Device

@method_decorator(legal_user, name='dispatch')
class DeviceList(TemplateView):
    template_name = 'home/device_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = Device.objects.all()
        context['devices_json'] = serializers.serialize("json", context['devices'])
        return context  

@method_decorator(legal_staff_user, name='dispatch')
class DeviceCreate(CreateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = ['name', 'longitude', 'latitude', 'ssh_pub']

    def form_valid(self, form):
        if not UpdatePubKey(form.instance.name, form.instance.ssh_pub).add():
            return HttpResponseRedirect(reverse('device_edit_fail', kwargs={'pk': form.instance.name}))
        
        cache.set(form.instance.name, str(form.instance.token), timeout=None)
        
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        return reverse('device_update', kwargs={'pk': self.object.name})

@method_decorator(legal_staff_user, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = ['longitude', 'latitude', 'ssh_pub']

    def form_valid(self, form):
        
        if not UpdatePubKey(form.instance.name, form.instance.ssh_pub).update():
            Device.objects.filter(name=form.instance.name).update(ssh_pub='')
            return HttpResponseRedirect(reverse('device_edit_fail', kwargs={'pk': form.instance.name}))
        
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('device_list')

@method_decorator(legal_staff_user, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'home/delete_device.html'
        
    def get_success_url(self):
        UpdatePubKey(self.object.name).delete()
        cache.delete(self.object.name)
        return reverse('device_list')

@method_decorator(legal_staff_user, name='dispatch')
class DeviceEditFail(TemplateView):
    template_name = 'home/edit_device_err.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_name'] = kwargs['pk']
        return context

##

@method_decorator(legal_staff_user, name='dispatch')
class ResetToken(View):

    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):        
        if not Device.objects.filter(name=kwargs['pk']).exists():
            raise Http404('Page Not Found')
        
        new_token = uuid.uuid4()
        Device.objects.filter(name=kwargs['pk']).update(token=new_token)
        cache.set(kwargs['pk'], str(new_token), timeout=None)

        return HttpResponseRedirect(reverse('device_update', kwargs={'pk': kwargs['pk']}))

##

class UpdatePubKey:
    def __init__(self, device_name, ssh_pub=None):
        self.path = settings.SSH_KEY_PATH
        self.comment = device_name
        self.key = ssh_pub

    def add(self):
        if not self._validate_SSH(self.key):
            return False
        
        try:
            # Check if the key's comment already exist
            with open(self.path, "r") as f:
                key_file = AuthorizedKeysFile(f, strict=False)
                comments = [i.comment for i in key_file.keys]
                if self.comment in comments:
                    return False

            """
            Change the key's comment into device_name and Append to the file:
            ssh-rsa [key] [device_name]
            """
            new_key = ' '.join(self.key.strip(' ').split(' ')[0:2] + [self.comment]) 
            with open(self.path, "a") as f:
                f.write(new_key + '\n')
            
            return True
        except:
            return False
    
    def update(self):
        self.delete()
        return self.add()

    def delete(self):
        cmd = 'echo "$(sed \'/.* {0}$/d\' {1})" > {1}'.format(self.comment, self.path)
        return subprocess.call(cmd, shell=True)

    def _validate_SSH(self, key):
        ssh = SSHKey(key, strict=True)
        try:
            ssh.parse()
        except:
            return False
        return True