import os
import datetime
from django.utils import timezone

from django.views.generic import TemplateView
from .views_decorator import *

from django.http import Http404
from django.conf import settings

from .models import Device

@method_decorator(legal_user, name='dispatch')
class DeviceInfoHistory(TemplateView):
    template_name = 'home/device_info_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not Device.objects.filter(pk=kwargs.get('pk')).exists():
            raise Http404
        
        context['device_id'] = kwargs.get('pk')
        context['vod_url'] = settings.VOD_URL
        return context

@ajax # -> would catch exceptions
@csrf_protect
@login_required
@verified_email_required
def get_history_info(request):
    if request.method != 'POST':
        raise Http404

    pk = request.POST.get('pk', None)
    ts = request.POST.get('ts', None)
    
    if pk == None or ts == None or not Device.objects.filter(pk=pk).exists():
        raise Http404
    
    ts = datetime.datetime.fromtimestamp(int(ts), datetime.timezone.utc)
    ts_next = ts + datetime.timedelta(hours=1)
    ts_last = ts - datetime.timedelta(minutes=settings.VOD_LEN) + datetime.timedelta(seconds=1)

    ## Get possible filenames
    filenames = sorted([
        int(
            i.name.replace('{}-'.format(pk), '')\
                  .replace(settings.VOD_EXT, '')
        ) 
        for i in os.scandir(os.path.join(settings.VOD_DIR, pk))
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
        
        data[i]['vod'] = '{}-{}{}'.format(pk, names[-1], settings.VOD_EXT) if names else ''
        data[i]['timestamp'] = timezone.localtime(ts_i).strftime('%Y-%m-%d %H:%M:%S %z')

    return data