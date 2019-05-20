import os
import uuid
import json
import datetime
from django.utils import timezone

from django.views import View
from django.views.generic import TemplateView
from .views_decorator import *
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

from django.core.cache import cache
from django.conf import settings

from .models import Device

##
from functools import wraps

def check_api_token(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
        except:
            return HttpResponseBadRequest()
        
        if request.user.is_authenticated or (
            data.get('token') != None and 
            data.get('token') == cache.get(data.get('user'))
        ):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return wrap
##

@method_decorator(legal_user, name='dispatch')
class OpenDataAPI(TemplateView):
    template_name = 'home/opendata.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        token = cache.get(self.request.user)
        if token == None:
            token = uuid.uuid4()
            cache.set(self.request.user, str(token), settings.API_TOKEN_TIMEOUT)
        
        ttl = cache.ttl(self.request.user)

        context['api_token'] = token
        context['api_token_ttl'] = ttl
        return context

@method_decorator(legal_user + [csrf_protect], name='dispatch')
class ResetAPIToken(View):
    
    def post(self, request, **kwargs):
        cache.set(request.user, str(uuid.uuid4()), settings.API_TOKEN_TIMEOUT)
        return HttpResponseRedirect(reverse('opendata'))

@method_decorator([csrf_exempt, check_api_token], name='dispatch')
class APIDevice(View):
    def post(self, request, **kwargs):
        return JsonResponse(list(Device.objects.all().values('id', 'longitude', 'latitude')), safe=False)

@method_decorator([csrf_exempt, check_api_token], name='dispatch')
class APIHistory(View):
    
    def post(self, request, **kwargs):
        pk = kwargs.get('pk')

        data = json.loads(request.body.decode("utf-8"))
        ts = data.get('ts_begin', None)
        ts_next = data.get('ts_end', None)
        
        if pk == None or ts == None or ts_next == None or not Device.objects.filter(pk=pk).exists():
            raise Http404
        
        ts = datetime.datetime.fromtimestamp(int(ts), datetime.timezone.utc)
        ts_next = datetime.datetime.fromtimestamp(int(ts_next), datetime.timezone.utc)

        data = Device.objects.get(pk=pk).info_history.filter(
            timestamp__gte=(timezone.localtime(ts)),
            timestamp__lt=(timezone.localtime(ts_next)),
        ).values()

        if request.is_ajax():
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

            for i in range(len(data)):
                ts_i = data[i]['timestamp']
                ts_i_int = int(ts_i.strftime('%s'))
                
                names = [name for name in filenames if ts_i_int in range(name, name + datetime.timedelta(minutes=settings.VOD_LEN).seconds)]
                
                data[i]['vod'] = '{}-{}{}'.format(pk, names[-1], settings.VOD_EXT) if names else ''
                data[i]['timestamp'] = timezone.localtime(ts_i).strftime('%Y-%m-%d %H:%M:%S %z')
        else:
            for i in range(len(data)):
                ts_i = data[i]['timestamp']
                data[i]['timestamp'] = timezone.localtime(ts_i)

        return JsonResponse(list(data), safe=False)