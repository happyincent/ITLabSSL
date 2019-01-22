from django.contrib import admin

# Register your models here.

from .models import Device, HistoryInfo

admin.site.register(Device)
admin.site.register(HistoryInfo)