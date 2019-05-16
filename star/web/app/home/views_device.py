import os
import subprocess
import uuid
import urllib.request
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

##
from django.contrib.auth.mixins import UserPassesTestMixin

class CheckOwnerMixin(UserPassesTestMixin):

    # Class View already deal with device (pk) not exist
    def test_func(self):
        return self.request.user.is_superuser or (
            Device.objects.get(
                pk = self.request.resolver_match.kwargs.get('pk')
            ).user.username == self.request.user.username
        )
##

@method_decorator(legal_user, name='dispatch')
class DeviceList(TemplateView):
    template_name = 'home/device_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = Device.objects.all()
        context['devices_json'] = serializers.serialize("json", context['devices'])
        return context

##

@method_decorator(legal_staff_user, name='dispatch')
class DeviceCreate(CreateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = ['id', 'longitude', 'latitude', 'ssh_pub']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setup_msg'] = settings.SETUP_MSG
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        if not UpdatePubKey(form.instance.id, form.instance.ssh_pub).add():
            form.instance.ssh_pub = None
        
        cache.set(form.instance.id, str(form.instance.token), timeout=None)
        
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        return reverse('device_update', kwargs={'pk': self.object.id})

##

@method_decorator(legal_staff_user, name='dispatch')
class DeviceUpdate(CheckOwnerMixin, UpdateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = ['longitude', 'latitude', 'ssh_pub']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setup_msg'] = settings.SETUP_MSG
        return context

    def form_valid(self, form):
        
        if not UpdatePubKey(form.instance.id, form.instance.ssh_pub).update():
            Device.objects.filter(pk=form.instance.id).update(ssh_pub='')
            return HttpResponseRedirect(reverse('device_edit_fail', kwargs={'pk': form.instance.id}))

        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('device_list')

@method_decorator(legal_staff_user, name='dispatch')
class DeviceDelete(CheckOwnerMixin, DeleteView):
    model = Device
    template_name = 'home/delete_device.html'
        
    def get_success_url(self):
        UpdatePubKey(self.object.id).delete()        
        cache.delete(self.object.id)

        # dangerous: ensure quoted appropriately to avoid shell injection
        subprocess.call('rm -rf {}*'.format(os.path.join(settings.VOD_DIR, self.object.id)), shell=True)

        # Drop RTMP connection
        urllib.request.urlopen(settings.RTMP_DROP_URL.format(self.object.id))

        return reverse('device_list')

@method_decorator(legal_staff_user + [csrf_protect], name='dispatch')
class ResetToken(CheckOwnerMixin, View):

    def post(self, request, **kwargs):
        if not Device.objects.filter(pk=kwargs.get('pk')).exists():
            raise Http404
        
        new_token = uuid.uuid4()
        Device.objects.filter(pk=kwargs.get('pk')).update(token=new_token)
        cache.set(kwargs.get('pk'), str(new_token), timeout=None)

        # Drop RTMP connection
        urllib.request.urlopen(settings.RTMP_DROP_URL.format(kwargs.get('pk')))

        return HttpResponseRedirect(reverse('device_update', kwargs={'pk': kwargs.get('pk')}))

##

@method_decorator(legal_staff_user, name='dispatch')
class DeviceEditFail(TemplateView):
    template_name = 'home/edit_device_err.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = kwargs.get('pk')
        return context

##

class UpdatePubKey:
    def __init__(self, device_id, ssh_pub=None):
        self.path = settings.SSH_KEY_PATH
        self.comment = device_id
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
            Change the key's comment into device_id and Append to the file:
            ssh-rsa [key] [device_id]
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
        # dangerous: ensure quoted appropriately to avoid shell injection
        cmd = 'echo "$(sed \'/.* {0}$/d\' {1})" > {1}'.format(self.comment, self.path)
        return subprocess.call(cmd, shell=True)

    def _validate_SSH(self, key):
        ssh = SSHKey(key, strict=True)
        try:
            ssh.parse()
        except:
            return False
        return True
