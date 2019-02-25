from django.urls import path

from . import views
from . import views_device
from . import views_now
from . import views_history
from . import views_nginx_rtmp

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('aboutus', views.Aboutus.as_view(), name='aboutus'),
    
    path('device_list', views_device.DeviceList.as_view(), name='device_list'),
    path('device_create', views_device.DeviceCreate.as_view(), name='device_create'),
    path('device_update/<slug:pk>', views_device.DeviceUpdate.as_view(), name='device_update'),
    path('device_delete/<slug:pk>', views_device.DeviceDelete.as_view(), name='device_delete'),
    path('device_edit_fail/<slug:pk>', views_device.DeviceEditFail.as_view(), name='device_edit_fail'),
    path('reset_token/<slug:pk>', views_device.ResetToken.as_view(), name='reset_token'),

    # channels' url is defined in app/star/routing/application
    path('device/<slug:pk>', views_now.DeviceInfo.as_view(), name='device'),
    path('key/<str:path>', views_now.key, name='key'),

    path('device_history/<slug:pk>', views_history.DeviceInfoHistory.as_view(), name='device_history'),
    path('get_history_info', views_history.get_history_info, name='get_history_info'),
    path('vod/<str:path>', views_history.Vod.as_view(), name='vod'),

    path('hooks/on_publish', views_nginx_rtmp.on_publish, name='on_publish'),
]