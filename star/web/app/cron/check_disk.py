import os
import psutil
import datetime

from django_cron import CronJobBase, Schedule
from django.conf import settings

class LimitDiskUsage(CronJobBase):

    schedule = Schedule(run_at_times=settings.CHECK_DISK_USAGE_AT)
    code = 'cron.check_disk.LimitDiskUsage'

    def do(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        try:
            curr = psutil.disk_usage(settings.VOD_DIR).percent
            
            if curr >= settings.MAX_DISK_USAGE_PERCENT:
                files = [
                    file for file in os.listdir(settings.VOD_DIR) 
                    if os.path.isfile(os.path.join(settings.VOD_DIR, file)) and
                       os.path.splitext(file)[1] == settings.VOD_EXT
                ]
                del_files = files[0 : int(len(files) * settings.DEL_OLDEST_VOD_PERCENT)]
                
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