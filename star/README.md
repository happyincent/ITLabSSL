# star

## Enviornment

```
$ cat <(echo "OS:     " `lsb_release -d | cut -f2`) <(echo "Kernel: " `uname -a | cut -d' ' -f1,3,14`) <(docker --version) <(docker-compose --version)
OS:      Ubuntu 16.04.6 LTS
Kernel:  Linux 4.15.0-45-generic x86_64
Docker version 18.09.2, build 6247962
docker-compose version 1.23.2, build 1110ad01
```

## Installation
[INSTALL.md](/INSTALL.md)

## Run without `supervisord`
```
# Comment out "supervisorctl start xxx" in web/run.sh
# docker-compose restart web

docker exec -it web-star gunicorn star.wsgi:application -c gunicorn.config.py
docker exec -it web-star daphne -b 0.0.0.0 -p 8001 --proxy-headers star.asgi:application

docker exec -it web-star python manage.py runserver 0.0.0.0:8000
```

## Init letsencrypt for the first time
```
# Check nginx's volumes with nginx_init.conf in docker-compose.yml
docker-compose up -d --no-deps nginx
docker-compose up -d --no-deps letsencrypt

# Comment nginx_init.conf and use nginx.conf in docker-compose.yml
docker-compose up -d
```

## Backup & Restore data
```
# git clone git@itlab7f.ddns.net:ddl/star.git

# backup
sudo tar -cvpf ~/Desktop/backup-star-data.tar db/data/ sshd/host_keys

# restore
sudo tar --same-owner -xvf ~/Desktop/backup-star-data.tar
```