#!/bin/sh

# Record pipdeptree
_required=`mktemp`
_installed=`mktemp`
cat /www/requirements.txt | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'[' -f1 | sed -e '/^#/d' -e '/^$/d' > $_required
pip freeze > $_installed
sed -i '/^##/d' /www/requirements.txt
grep -F -f $_required $_installed | sed -e 's/djongo/djongo[json]/' -e 's/^/## /g' >> /www/requirements.txt
rm $_required $_installed
pipdeptree > /www/pipdeptree.txt

# migrage DB
python /www/manage.py makemigrations
python /www/manage.py migrate
python /www/manage.py migrate django_cron

# collect static files
find /www/home/static/home/plugin/ -type f -exec sed -i '/sourceMappingURL/d' {} \;
python /www/manage.py collectstatic --noinput

# load and start supervisord jobs
supervisord -c /etc/supervisord.conf
supervisorctl start gunicorn
supervisorctl start daphne

# setup permission
chmod 644 /logrotate.conf
chown root:root /logrotate.conf

# load crontab and start in foreground
cat /crontab > /var/spool/cron/crontabs/root
crond -f

# tail -f /dev/null