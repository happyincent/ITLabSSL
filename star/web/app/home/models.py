from django.db import models
from django.urls import reverse

# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    longitude = models.FloatField(default=120.224)
    latitude = models.FloatField(default=22.996)
    uri = models.CharField(max_length=200, unique=True)

    def info_url(self):
        return reverse('device', kwargs={'device_name': self.name})
    
    def history_url(self):
        return reverse('device_history', kwargs={'device_name': self.name})
    def update_url(self):
        return reverse('device_update', kwargs={'pk': self.pk})
    
    def delete_url(self):
        return reverse('device_delete', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.name

# class DeviceInfo(models.Model):
#     device_name = models.ForeignKey(Device, related_name='infos', on_delete=models.CASCADE)
#     temperature = models.FloatField(default=0.0)
#     humidity = models.FloatField(default=0.0)
#     pm2_5 = models.FloatField(default=0.0)
#     loudness = models.FloatField(default=0.0)
#     light_intensity = models.FloatField(default=0.0)
#     uv_intensity = models.FloatField(default=0.0)
#     ir_sensed = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return '{}-{}'.format(self.device_name.pk, self.timestamp.strftime('%s'))