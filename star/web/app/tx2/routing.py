from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/browser/device/<slug:device_name>', consumers.InfoConsumer),
    path('ws/light/device/<slug:device_name>', consumers.InfoConsumer),
]