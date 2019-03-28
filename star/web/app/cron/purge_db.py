import datetime
from django.utils import timezone

from django_cron import CronJobBase, Schedule
from django.conf import settings

from home.models import HistoryInfo

class PurgeOldHistory(CronJobBase):

    schedule = Schedule(run_at_times=settings.PURGE_DB_AT)
    code = 'cron.purge_db.PurgeOldHistory'

    def do(self):
        ts = datetime.datetime.now(datetime.timezone.utc)
        now = ts.strftime('%Y-%m-%d %H:%M:%S')
        ts_oldest = ts - datetime.timedelta(weeks = int(settings.PURGE_HISTORY_OLDER_WEEKS))

        try:
            data = HistoryInfo.objects.filter(timestamp__lt=(timezone.localtime(ts_oldest)))
            data_count = data.count()

            if data_count > 0:
                data.delete()
                print('PurgeOldHistory: delete {} data ... {}'.format(data_count, now))
                return 'PurgeOldHistory: delete {} data ... {}'.format(data_count, now)
            
            else:
                print('PurgeOldHistory: delete 0 data ... {}'.format(now))
                return 'PurgeOldHistory: delete 0 data ... {}'.format(now)
        except Exception as e:
            print('PurgeOldHistory: FAIL: {} ... {}'.format(e, now))
            return 'PurgeOldHistory: FAIL: {} ... {}'.format(e, now)