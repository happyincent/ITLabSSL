from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('device', views.Device.as_view(), name='device'),
    path('add_device', views.AddDevice.as_view(), name='add_device'),
    path('key/<str:stream>', views.key, name='key'),
]