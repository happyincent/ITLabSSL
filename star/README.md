# star

## Installation
[INSTALL.md](/doc/INSTALL.md)

### Init letsencrypt for the first time
```
# docker-compose.yml -> nginx -> volumes: nginx_init.conf
docker-compose up -d --no-deps nginx
docker-compose up --no-deps certbot
(Ctrl+C)

# docker-compose.yml -> nginx -> volumes: nginx.conf
docker-compose up -d
```

### Configuration
[CONFIG.md](/doc/CONFIG.md)

#### Change Site Information
Navigate to `/admin/sites/site/1/change/` with the superuser account.

---

## Usage
`(sudo) docker-compose up -d`

### Debugging
```
docker exec -it web-star sh

# For http
supervisorctl stop gunicorn
python manage.py runserver 0.0.0.0:8000

# For websocket
supervisorctl stop daphne
python manage.py runserver 0.0.0.0:8001
```

---

## Backup & Restore
```
# Backup
sudo bash doc/backup.sh

# Restore (warning: it will remove star project!)
sudo bash doc/restore.sh
```