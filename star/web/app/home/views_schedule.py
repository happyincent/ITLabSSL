import json

from django.views.generic import TemplateView
from .views_decorator import *

from django.http import Http404
from django.core import serializers

from .models import Device

@method_decorator(legal_staff_user, name='dispatch')
class DeviceSchedule(TemplateView):
    template_name = 'home/led_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if not Device.objects.filter(pk=kwargs.get('pk')).exists():
            raise Http404
        
        context['device_id'] = kwargs.get('pk')
        
        device = Device.objects.filter(pk=kwargs.get('pk'))
        context['device'] = serializers.serialize("json", device)
        
        return context