# star

## Installation
[INSTALL.md](/doc/INSTALL.md)

### Init letsencrypt for the first time
```
# docker-compose.yml -> nginx -> volumes: nginx_init.conf
docker-compose up -d --no-deps nginx
docker-compose up --no-deps letsencrypt
(Ctrl+C)

# docker-compose.yml -> nginx -> volumes: nginx.conf
docker-compose up -d
```

### Backup & Restore
```
# git
git clone git@itlab7f.ddns.net:ddl/star.git

# backup
sudo tar -cvpf ~/Desktop/backup-star-data.tar db/data/ sshd/host_keys

# restore (username=itlab)
sudo tar --same-owner -xvf ~/Desktop/backup-star-data.tar
```

### Configuration
[CONFIG.md](/doc/CONFIG.md)

## Usage
`(sudo) docker-compose up -d`

### Run without `supervisord`
```
# 1. Comment out "supervisorctl start xxx" in web/run.sh
# 2. Restart: docker-compose restart web

# For http request
docker exec -it web-star python manage.py runserver 0.0.0.0:8000
## or
docker exec -it web-star gunicorn -b 0.0.0.0:8000 --workers 4 --worker-class 'gevent' --access-logfile '-' star.wsgi:application

# For http websocket
docker exec -it web-star daphne -b 0.0.0.0 -p 8001 --proxy-headers --access-log '-' star.asgi:application
```