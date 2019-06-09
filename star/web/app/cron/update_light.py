import datetime

from django_cron import CronJobBase, Schedule
from django.utils import timezone
from django.conf import settings

from home.models import Device

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class UpdateLight(CronJobBase):
    RUN_EVERY_MINS = settings.UPDATE_LIGHT_EVERY_MINS
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES)
    code = 'cron.update_light.UpdateLight'

    def do(self):
        utc_now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        now = timezone.localtime(timezone.now())
        now_week = now.isoweekday()
        now_time = now.time()

        try:
            channel_layer = get_channel_layer()

            for device in Device.objects.all():
                
                led_schedule_time = [
                    (
                        datetime.datetime.strptime(i['start'], '%H:%M').time(),
                        datetime.datetime.strptime(i['end'], '%H:%M').time() if i['end'] != '00:00' else datetime.time(23, 59)
                    )
                    for i in device.led_schedule[now_week-1]['periods']
                ]

                pir_schedule_time = [
                    (
                        datetime.datetime.strptime(i['start'], '%H:%M').time(),
                        datetime.datetime.strptime(i['end'], '%H:%M').time() if i['end'] != '00:00' else datetime.time(23, 59)
                    )
                    for i in device.pir_schedule[now_week-1]['periods']
                ]

                led_check_lst = [(period[0] <= now_time < period[1]) for period in led_schedule_time]
                pir_check_lst = [(period[0] <= now_time < period[1]) for period in pir_schedule_time]

                # LED first
                async_to_sync(channel_layer.group_send)(device.id, {
                    'type': 'broatcast_json', 'content': {
                        'cmd': 'led_ctrl', 'data': {'led_status': 1 if True in led_check_lst else 0}
                    }
                })

                async_to_sync(channel_layer.group_send)(device.id, {
                    'type': 'broatcast_json', 'content': {
                        'cmd': 'pir_ctrl', 'data': {'pir_status': 1 if True in pir_check_lst else 0}
                    }
                })

            print('UpdateLight SUCCESS ... {}'.format(utc_now))
            return 'UpdateLight SUCCESS ... {}'.format(utc_now)
        except Exception as e:
            print('UpdateLight FAIL: {} ... {}'.format(e, utc_now))
            return 'UpdateLight FAIL: {} ... {}'.format(e, utc_now)