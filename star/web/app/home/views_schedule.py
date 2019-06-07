import json

from django.views import View
from django.views.generic import TemplateView
from .views_decorator import *

from django.http import Http404, JsonResponse
from django.core import serializers

from .models import Device

@method_decorator(legal_staff_user, name='dispatch')
class DeviceSchedule(TemplateView):
    template_name = 'home/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if not Device.objects.filter(pk=kwargs.get('pk')).exists():
            raise Http404
        
        device = Device.objects.filter(pk=kwargs.get('pk'))
        context['device'] = serializers.serialize("json", device)
        
        return context

@method_decorator(legal_staff_user, name='dispatch')
class DeviceScheduleUpdate(View):
    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        table = kwargs.get('table')
        
        if not Device.objects.filter(pk=pk).exists():
            raise Http404

        data = json.loads(request.body.decode("utf-8"))
        data = json.loads(data)

        if table == 'led':
            Device.objects.filter(pk=pk).update(led_schedule=data)
        elif table == 'pir':
            Device.objects.filter(pk=pk).update(pir_schedule=data)

        return JsonResponse(data, safe=False)