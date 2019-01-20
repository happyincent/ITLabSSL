from django.db import models

# Create your models here.
from home.models import Device

class DeviceInfoNow(models.Model):
    device = models.ForeignKey(Device, related_name='infos', on_delete=models.CASCADE)
    temperature = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    pm2_5 = models.FloatField(default=0.0)
    loudness = models.FloatField(default=0.0)
    light_intensity = models.FloatField(default=0.0)
    uv_intensity = models.FloatField(default=0.0)
    ir_sensed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.device.pk, self.timestamp.strftime('%s'))