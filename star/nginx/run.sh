#!/bin/sh

# setup permission
chmod 644 /logrotate.conf
chown root:root /logrotate.conf

# remove & load & start crontab (in background)
find /etc/periodic/ -type f -exec rm {} \;
cat /crontab > /var/spool/cron/crontabs/root
crond -b

# if fullchain.pem exist && dhparam.pem not exist -> generate DH key (might take a "long" time)
test -f /etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/fullchain.pem && \
test ! -f /etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/dhparam.pem && \
openssl dhparam 4096 -out /etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/dhparam.pem

# run nginx foreground
nginx -g 'daemon off;'