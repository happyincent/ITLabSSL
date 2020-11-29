from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, HttpResponse
from django.core.cache import cache

from .models import Device
from allauth.account.models import EmailAddress

@csrf_exempt
def on_publish(request):
    if request.method == 'POST':
        id = request.POST.get('name', None) # nginx-rtmp use "name"
        token = request.POST.get('token', None)

        if id != None and token != None and cache.get(id) == token:
            return HttpResponse(status=200)

    return HttpResponseForbidden()

def check_user(request):
    if request.user.is_authenticated and EmailAddress.objects.filter(user=request.user, verified=True).exists():
        return HttpResponse(status=200)
    return HttpResponseForbidden()