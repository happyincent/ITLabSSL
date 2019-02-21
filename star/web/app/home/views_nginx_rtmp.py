from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.cache import cache

from .models import Device

@csrf_exempt
def on_publish(request):
    if request.method == 'POST':
        token = request.POST.get('token', None)
        name = request.POST.get('name', None)

        if name != None and token != None and cache.get(name) == token:
            return HttpResponse(status=200)

    return HttpResponse(status=403)