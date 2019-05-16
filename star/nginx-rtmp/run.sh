#!/bin/sh

# setup permission
chmod 644 /logrotate.conf
chown root:root /logrotate.conf

# load crontab and start in background
cat /crontab > /var/spool/cron/crontabs/root
crond -b

# run nginx foreground
nginx -g 'daemon off;'