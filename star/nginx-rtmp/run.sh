#!/bin/sh

# setup permission
chmod 644 /logrotate.conf
chown root:root /logrotate.conf

# remove & load & start crontab (in background)
find /etc/periodic/ -type f -exec rm {} \;
cat /crontab > /var/spool/cron/crontabs/root
crond -b

# run nginx foreground
nginx -g 'daemon off;'