from django.urls import path

from . import consumers

websocket_urlpatterns = [
    # block request if (device_type == edge) in nginx (allow only from ssh tunnel)
    path('ws/<slug:client_type>/device/<slug:device_id>', consumers.StarConsumer),
]