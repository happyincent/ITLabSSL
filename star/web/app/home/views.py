from django.views.generic import TemplateView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'home/home.html'

###

import os
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

HLS_KEY_DIR = '/tmp/key'

@login_required
def key(request, stream):
    file_path = os.path.join(HLS_KEY_DIR, stream)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/octet-stream')
    raise Http404