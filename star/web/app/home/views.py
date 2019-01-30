import os
import uuid

import datetime
from django.utils import timezone

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse, reverse_lazy

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.views import View
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
    
from django.contrib.auth.models import User

@method_decorator(decorator_legal_user, name='dispatch')
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

@method_decorator(decorator_legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    template_name = 'home/edit_device.html'
    fields = ['longitude', 'latitude', 'ssh_pub']
    
    def get_success_url(self):
        return reverse('device_list')

@method_decorator(decorator_legal_user, name='dispatch')
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


@method_decorator(decorator_legal_user, name='dispatch')
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

@method_decorator(decorator_legal_user, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class DeviceEditFail(TemplateView):
    template_name = 'home/device_err.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_name'] = kwargs['pk']
        return context

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
def key(request, path):
    file_path = os.path.join(HLS_KEY_DIR, path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/octet-stream')
    raise Http404

@method_decorator(decorator_legal_user, name='dispatch')
class Vod(ProxyView):
    upstream = 'http://nginx:62401/record/'


# class Live(ProxyView):
#     upstream = 'http://nginx:62401/hls/'
    
#     def _created_proxy_response(self, request, path):
#         request_payload = request.body

#         self.log.debug("Request headers: %s", self.request_headers)

#         path = self.get_quoted_path(path)
#         path = to_streamKey(path)

#         request_url = self.get_upstream(path) + path
#         self.log.debug("Request URL: %s", request_url)

#         if request.GET:
#             request_url += '?' + self.get_encoded_query_params()
#             self.log.debug("Request URL: %s", request_url)

#         try:
#             proxy_response = self.http.urlopen(request.method,
#                                                request_url,
#                                                redirect=False,
#                                                retries=self.retries,
#                                                headers=self.request_headers,
#                                                body=request_payload,
#                                                decode_content=False,
#                                                preload_content=False)
#             self.log.debug("Proxy response header: %s",
#                            proxy_response.getheaders())
#         except urllib3.exceptions.HTTPError as error:
#             self.log.exception(error)
#             raise

#         return proxy_response

# def to_streamKey(path):
#     streamID = '.'.join(path.split('.')[:-1])

#     if not Device.objects.filter(pk=streamID).exists():
#         return path
#     return path.replace(streamID, Device.objects.get(pk=streamID).name)