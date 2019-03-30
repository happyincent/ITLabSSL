import datetime
import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Device(models.Model):
    user = models.ForeignKey(User, default=None, null=True, related_name='devices', on_delete=models.SET_DEFAULT)
    id = models.SlugField(max_length=20, verbose_name="Device ID", primary_key=True)
    longitude = models.FloatField(default=120.22283)
    latitude = models.FloatField(default=22.99672)
    token = models.UUIDField(default=uuid.uuid4)
    ssh_pub = models.CharField(default='ssh-rsa [key] [comment]', blank=True, max_length=1000, verbose_name="SSH Public Key")

    def info_url(self):
        return reverse('device', kwargs={'pk': self.pk})
    
    def history_url(self):
        return reverse('device_history', kwargs={'pk': self.pk})
    
    def update_url(self):
        return reverse('device_update', kwargs={'pk': self.pk})
    
    def delete_url(self):
        return reverse('device_delete', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.id

class HistoryInfo(models.Model):
    device = models.ForeignKey(Device, related_name='info_history', on_delete=models.CASCADE)
    temperature = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    pm2_5 = models.FloatField(default=0.0)
    loudness = models.FloatField(default=0.0)
    light_intensity = models.FloatField(default=0.0)
    uv_intensity = models.FloatField(default=0.0)
    ir_sensed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.datetime(1970,1,1))

    def __str__(self):
        return '{}-{}'.format(self.device.pk, self.timestamp.strftime('%s'))