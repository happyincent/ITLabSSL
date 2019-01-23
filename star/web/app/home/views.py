import os

import datetime
from django.utils import timezone

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
from django.views.decorators.csrf import csrf_protect

from revproxy.views import ProxyView
from django_ajax.decorators import ajax

from .models import Device

decorator_legal_user = [login_required, verified_email_required]

@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'home/home.html'

@method_decorator(decorator_legal_user, name='dispatch')
class Aboutus(TemplateView):
    template_name = 'home/aboutus.html'

###

@method_decorator(decorator_legal_user, name='dispatch')
class DeviceList(TemplateView):
    template_name = 'home/device_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = Device.objects.all()
        context['devices_json'] = serializers.serialize("json", context['devices'])
        return context

@method_decorator(decorator_legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceCreate(CreateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = '__all__'

    def get_success_url(self):
        print(self.object.name)
        return reverse('device_list')

@method_decorator(decorator_legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = ['longitude', 'latitude', 'uri']
    
    def get_success_url(self):
        print(self.object.name)
        return reverse('device_list')

@method_decorator(decorator_legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'home/delete_device.html'
    success_url = reverse_lazy('device_list')

###

@method_decorator(decorator_legal_user, name='dispatch')
class DeviceInfo(TemplateView):
    template_name = 'home/device_info_now.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if not Device.objects.filter(pk=kwargs['pk']).exists():
            raise Http404('Page Not Found')
        
        context['device_name'] = kwargs['pk']
        context['device_info'] = Device.objects.get(pk=kwargs['pk']).info_now.first()
        return context

@method_decorator(decorator_legal_user, name='dispatch')
class DeviceInfoHistory(TemplateView):
    template_name = 'home/device_info_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not Device.objects.filter(pk=kwargs['pk']).exists():
            raise Http404('Page Not Found')
        
        context['device_name'] = kwargs['pk']
        return context

###

VOD_DIR = '/media/data/record'
VOD_EXT = '.mp4'
VOD_LEN = 15 # minutes

@ajax # -> would catch exceptions
@csrf_protect
@login_required
@verified_email_required
def get_history_info(request):
    if request.method != 'POST':
        raise Http404('Page Not Found')

    pk = request.POST.get('pk', None)
    ts = request.POST.get('ts', None)
    
    if pk == None or ts == None:
        raise Http404('Page Not Found')
    
    ts = datetime.datetime.fromtimestamp(int(ts), datetime.timezone.utc)
    ts_next = ts + datetime.timedelta(hours=1)
    ts_last = ts - datetime.timedelta(minutes=VOD_LEN) + datetime.timedelta(seconds=1)

    ## Get possible filenames
    filenames = sorted([
        int(
            e.name.replace('{}-'.format(pk), '')\
                  .replace(VOD_EXT, '')
        ) 
        for e in os.scandir(VOD_DIR)
        if e.name.startswith(pk) and e.name.endswith(VOD_EXT)
    ])

    filenames = [i for i in filenames if i in range(int(ts_last.strftime('%s')), int(ts_next.strftime('%s')))]
    ##

    data = Device.objects.get(pk=pk).info_history.filter(
        timestamp__gte=(timezone.localtime(ts)),
        timestamp__lt=(timezone.localtime(ts_next)),
    ).values()
    
    
    for i in range(len(data)):
        ts_i = data[i]['timestamp']
        ts_i_int = int(ts_i.strftime('%s'))
        
        names = [name for name in filenames if name <= ts_i_int]
        
        data[i]['vod'] = '{}-{}{}'.format(pk, names[-1], VOD_EXT) if names else ''
        data[i]['timestamp'] = timezone.localtime(ts_i).strftime('%Y-%m-%d %H:%M:%S %z')

    return data

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

@method_decorator(decorator_legal_user, name='dispatch')
class Vod(ProxyView):
    upstream = 'http://nginx:62401/record/'
