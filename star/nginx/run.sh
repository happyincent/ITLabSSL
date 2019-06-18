#!/bin/sh

# setup permission
chmod 644 /logrotate.conf
chown root:root /logrotate.conf

# remove & load & start crontab (in background)
find /etc/periodic/ -type f -exec rm {} \;
cat /crontab > /var/spool/cron/crontabs/root
crond -b

# make sure dhparam.pem exist
if [   -f /etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/fullchain.pem ] && \
   [ ! -f /etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/dhparam.pem ];
then
    echo "Generating DH key..."
    FILE=`mktemp`
    openssl dhparam -dsaparam -out $FILE 4096 2> /dev/null && cat $FILE > /etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/dhparam.pem
    echo "Generating DH key...OK"
fi

# run nginx foreground
nginx -g 'daemon off;'