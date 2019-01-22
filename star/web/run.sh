#!/bin/sh

python /www/manage.py makemigrations
python /www/manage.py migrate
python /www/manage.py migrate django_cron
python /www/manage.py collectstatic --noinput

cat /crontab > /var/spool/cron/crontabs/root && crond

tail -f /dev/null
# gunicorn star.wsgi:application -c /www/gunicorn.config.py