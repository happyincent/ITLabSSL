import datetime

from django_cron import CronJobBase, Schedule

from home.models import Device, HistoryInfo
from tx2.models import InstantInfo

from django.forms import model_to_dict

class UpdateHistory(CronJobBase):
    RUN_EVERY_MINS = 15
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES)
    code = 'cron.update.UpdateHistory'

    def do(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        try:
            for info in InstantInfo.objects.all():
                
                device = Device.objects.filter(pk=info.device.pk).first()
                if device == None:
                    continue
                
                latest = device.info_history.order_by('timestamp').first()
                
                if latest != None and info.timestamp == latest.timestamp:
                    print('{} same timestamp: {}'.format(device.pk, info.timestamp.strftime('%s')))
                    continue
                
                kwargs = model_to_dict(info, exclude=['id', 'device'])

                HistoryInfo.objects.create(device=device, timestamp=info.timestamp, **kwargs)
                
            print('UpdateHistory SUCCESS ... {}'.format(now))
        except Exception as e:
            print(e)
            print('UpdateHistory FAIL ... {}'.format(now))