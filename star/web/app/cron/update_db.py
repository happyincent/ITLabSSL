import pickle
import datetime

from django_cron import CronJobBase, Schedule
from django.utils import timezone
from django.conf import settings

from django.core.cache import cache
from home.models import Device, HistoryInfo

from django.forms import model_to_dict

class UpdateHistory(CronJobBase):
    RUN_EVERY_MINS = settings.UPDATE_HISTORY_EVERY_MINS
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES)
    code = 'cron.update_db.UpdateHistory'

    def do(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        try:
            for key in cache.keys("*{}".format(settings.INFO_POSTFIX)):
                
                device = Device.objects.filter(pk=key.replace(settings.INFO_POSTFIX, '')).first()
                if device == None:
                    continue
                
                info_last = device.info_history.order_by('-timestamp').first()
                info_now = pickle.loads(cache.get(key))
                
                ts = info_now.get('timestamp', None)

                if ts == None:
                    print('UpdateHistory: {} error timestamp'.format(device.pk))
                    continue

                if info_last != None and timezone.localtime(info_last.timestamp).strftime(settings.INFO_TIMESTR) == ts:
                    print('UpdateHistory: {}: same timestamp'.format(device.pk))
                    continue

                info_now['timestamp'] = datetime.datetime.strptime(ts, settings.INFO_TIMESTR)

                HistoryInfo.objects.create(device=device, **info_now)
                
            print('UpdateHistory SUCCESS ... {}'.format(now))
            return 'UpdateHistory SUCCESS ... {}'.format(now)
        except Exception as e:
            print('UpdateHistory FAIL: {} ... {}'.format(e, now))
            return 'UpdateHistory FAIL: {} ... {}'.format(e, now)