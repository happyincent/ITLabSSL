#!/bin/sh

python /www/manage.py makemigrations
python /www/manage.py migrate
python /www/manage.py migrate django_cron
python /www/manage.py collectstatic --noinput

supervisord -c /supervisord.conf
supervisorctl start gunicorn
supervisorctl start daphne

chmod 644 /logrotate.conf
chown root:root /logrotate.conf

cat /crontab > /var/spool/cron/crontabs/root
crond -f

# tail -f /dev/null