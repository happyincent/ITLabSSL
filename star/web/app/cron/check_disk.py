import os
import psutil

from django_cron import CronJobBase, Schedule
from django.conf import settings

class LimitDiskUsage(CronJobBase):
    RUN_AT_TIMES = settings.CHECK_DISK_USAGE_AT

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'cron.check_disk.LimitDiskUsage'

    def do(self):
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
            
                print('LimitDiskUsage: clean up {} files'.format(len(del_files)))
            
            print('LimitDiskUsage: SUCCESS without clean up files')
        except Exception as e:
            print('LimitDiskUsage FAIL: {}'.format(e))