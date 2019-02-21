import os
import datetime
from django.utils import timezone

from django.views.generic import TemplateView
from revproxy.views import ProxyView
from .views_decorator import *

from django.http import Http404

from .models import Device

VOD_DIR = '/media/data/record'
VOD_EXT = '.mp4'
VOD_LEN = 15 # minutes

@method_decorator(legal_user, name='dispatch')
class DeviceInfoHistory(TemplateView):
    template_name = 'home/device_info_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not Device.objects.filter(pk=kwargs['pk']).exists():
            raise Http404('Page Not Found')
        
        context['device_name'] = kwargs['pk']
        return context

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

@method_decorator(legal_user, name='dispatch')
class Vod(ProxyView):
    upstream = 'http://nginx:62401/record/'