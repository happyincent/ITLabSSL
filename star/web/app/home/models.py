from django.db import models
from django.urls import reverse

# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=200, unique=True)
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