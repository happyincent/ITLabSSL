from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/device/<str:device_name>/', consumers.InfoConsumer),
]