#!/bin/sh

cat /crontab > /var/spool/cron/crontabs/root
crond -b

nginx -g 'daemon off;'