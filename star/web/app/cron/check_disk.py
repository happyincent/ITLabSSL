import os
import psutil

from django.utils import timezone

from django_cron import CronJobBase, Schedule
from django.conf import settings

class LimitDiskUsage(CronJobBase):

    schedule = Schedule(run_at_times=settings.CHECK_DISK_USAGE_AT)
    code = 'cron.check_disk.LimitDiskUsage'

    def do(self):
        now = timezone.localtime(timezone.now()).replace(microsecond=0).isoformat()

        try:
            curr = psutil.disk_usage(settings.VOD_DIR).percent
            
            if curr >= settings.MAX_DISK_USAGE_PERCENT:
                files = [os.path.join(dp, f) for dp, dn, fn in os.walk(settings.VOD_DIR) for f in fn]
                files.sort(key=lambda i: os.path.getmtime(os.path.join(settings.VOD_DIR, i)))
                
                del_files = files[0 : int(len(files) * (settings.DEL_OLDEST_VOD_PERCENT / 100))]
                
                for file in del_files:
                    os.remove(os.path.join(settings.VOD_DIR, file))
            
                print('LimitDiskUsage: delete {} vods ... {}'.format(len(del_files), now))
                return 'LimitDiskUsage: delete {} vods ... {}'.format(len(del_files), now)
            
            else:
                print('LimitDiskUsage: delete 0 vods ... {}'.format(now))
                return 'LimitDiskUsage: delete 0 vods ... {}'.format(now)
        except Exception as e:
            print('LimitDiskUsage: FAIL: {} ... {}'.format(e, now))
            return 'LimitDiskUsage: FAIL: {} ... {}'.format(e, now)