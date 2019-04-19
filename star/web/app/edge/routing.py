from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/browser/device/<slug:device_id>', consumers.StarConsumer),
    
    # block request from edge by nginx (allow from edge by ssh encryption)
    path('ws/edge/device/<slug:device_id>', consumers.StarConsumer),
]