#!/bin/sh

chmod 644 /logrotate.conf
chown root:root /logrotate.conf

cat /crontab > /var/spool/cron/crontabs/root
crond -b

if [ ! -f /etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/dhparam.pem ]; then
    openssl dhparam 4096 -out /etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/dhparam.pem
fi

nginx -g 'daemon off;'