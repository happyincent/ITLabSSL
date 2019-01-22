from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('aboutus', views.Aboutus.as_view(), name='aboutus'),
    
    path('device_list', views.DeviceList.as_view(), name='device_list'),

    path('device_create', views.DeviceCreate.as_view(), name='device_create'),
    path('device_update/<slug:pk>', views.DeviceUpdate.as_view(), name='device_update'),
    path('device_delete/<slug:pk>', views.DeviceDelete.as_view(), name='device_delete'),

    path('device/<slug:pk>', views.DeviceInfo.as_view(), name='device'),
    path('device_history/<slug:pk>', views.DeviceInfoHistory.as_view(), name='device_history'),

    path('key/<str:stream>', views.key, name='key'),
    path('vod/<str:path>', views.Vod.as_view(), name='vod'),
]