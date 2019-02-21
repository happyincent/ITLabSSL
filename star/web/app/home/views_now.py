import os

from django.views.generic import TemplateView
from .views_decorator import *

from django.http import HttpResponse, Http404

from .models import Device

HLS_KEY_DIR = '/tmp/key'

@method_decorator(legal_user, name='dispatch')
class DeviceInfo(TemplateView):
    template_name = 'home/device_info_now.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if not Device.objects.filter(pk=kwargs['pk']).exists():
            raise Http404('Page Not Found')
        
        context['device_name'] = kwargs['pk']
        context['device_info'] = Device.objects.get(pk=kwargs['pk']).info_now.first()
        return context

@login_required
@verified_email_required
def key(request, path):
    file_path = os.path.join(HLS_KEY_DIR, path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/octet-stream')
    raise Http404


from revproxy.views import ProxyView

class Live(ProxyView):
    upstream = 'http://nginx:62401/hls/'
    
    def _created_proxy_response(self, request, path):
        request_payload = request.body

        self.log.debug("Request headers: %s", self.request_headers)

        path = self.get_quoted_path(path)
        path = to_streamKey(path)

        request_url = self.get_upstream(path) + path
        self.log.debug("Request URL: %s", request_url)

        if request.GET:
            request_url += '?' + self.get_encoded_query_params()
            self.log.debug("Request URL: %s", request_url)

        try:
            proxy_response = self.http.urlopen(request.method,
                                               request_url,
                                               redirect=False,
                                               retries=self.retries,
                                               headers=self.request_headers,
                                               body=request_payload,
                                               decode_content=False,
                                               preload_content=False)
            self.log.debug("Proxy response header: %s",
                           proxy_response.getheaders())
        except urllib3.exceptions.HTTPError as error:
            self.log.exception(error)
            raise

        return proxy_response

def to_streamKey(path):
    streamID = '.'.join(path.split('.')[:-1])

    if not Device.objects.filter(pk=streamID).exists():
        return path
    return path.replace(streamID, '298ff7d6-d741-4c15-8e75-da2179de338a')
    # return path.replace(streamID, Device.objects.get(pk=streamID).name)