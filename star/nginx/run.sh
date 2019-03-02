#!/bin/sh

# setup permission
chmod 644 /logrotate.conf
chown root:root /logrotate.conf

# load crontab and start in background
cat /crontab > /var/spool/cron/crontabs/root
crond -b

# check DH key
if [ ! -f /etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/dhparam.pem ]; then
    openssl dhparam 4096 -out /etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/dhparam.pem
fi

# run nginx foreground
nginx -g 'daemon off;'