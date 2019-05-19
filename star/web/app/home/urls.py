from django.urls import path

from . import views
from . import views_api
from . import views_device
from . import views_now
from . import views_history
from . import views_nginx

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('aboutus', views.Aboutus.as_view(), name='aboutus'),
    
    path('opendata', views_api.OpenDataAPI.as_view(), name='opendata'),
    path('api/reset_token', views_api.ResetAPIToken.as_view(), name='reset_api_token'),
    
    path('api/device', views_api.APIDevice.as_view(), name='api_device'),
    path('api/history/<slug:pk>', views_api.APIHistory.as_view(), name='api_history'),
    
    path('device_list', views_device.DeviceList.as_view(), name='device_list'),
    path('my_devices/<username>', views_device.MyDevices.as_view(), name='my_devices'),

    path('device_create', views_device.DeviceCreate.as_view(), name='device_create'),
    path('device_update/<slug:pk>', views_device.DeviceUpdate.as_view(), name='device_update'),
    path('device_delete/<slug:pk>', views_device.DeviceDelete.as_view(), name='device_delete'),
    path('device_edit_fail/<slug:pk>', views_device.DeviceEditFail.as_view(), name='device_edit_fail'),
    path('reset_token/<slug:pk>', views_device.ResetToken.as_view(), name='reset_token'),

    # channels' url is defined in app/star/routing/application
    path('device/<slug:pk>', views_now.DeviceInfo.as_view(), name='device'),
    path('history/<slug:pk>', views_history.DeviceInfoHistory.as_view(), name='device_history'),

    path('hooks/on_publish', views_nginx.on_publish, name='on_publish'),
    path('check_user', views_nginx.check_user, name='check_user'),
]