from django.db import models
from django.urls import reverse

# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=200, unique=True)
    longitude = models.FloatField(default=120.2241557)
    latitude = models.FloatField(default=22.9960156)
    uri = models.CharField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse('device', kwargs={'name': self.name})
    
    def __str__(self):
        return self.name