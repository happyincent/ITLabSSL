from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('device_list', views.DeviceList.as_view(), name='device_list'),
    path('device', views.DeviceInfo.as_view(), name='device'),
    path('device/<slug:name>', views.DeviceInfo.as_view(), name='device'),
    path('device_create', views.DeviceCreate.as_view(), name='device_create'),
    path('device_update/<int:pk>', views.DeviceUpdate.as_view(), name='device_update'),
    path('device_delete/<int:pk>', views.DeviceDelete.as_view(), name='device_delete'),
    path('key/<str:stream>', views.key, name='key'),
]