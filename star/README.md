# star

## Enviornment

```
$ cat <(echo "OS:     " `lsb_release -d | cut -f2`) <(echo "Kernel: " `uname -a | cut -d' ' -f1,3,14`) <(docker --version) <(docker-compose --version)
OS:      Ubuntu 16.04.5 LTS
Kernel:  Linux 4.15.0-45-generic x86_64
Docker version 18.09.2, build 6247962
docker-compose version 1.22.0, build f46880fe
```

## Run without `supervisord`
```
docker exec -it web-star gunicorn star.wsgi:application -c gunicorn.config.py
docker exec -it web-star daphne -b 0.0.0.0 -p 8001 --proxy-headers star.asgi:application

docker exec -it web-star python manage.py runserver 0.0.0.0:8000
```

## Backup & Restore data
```
# git clone git@itlab7f.ddns.net:ddl/star.git
# copy backup.tar into star/

# backup
sudo tar -cvpf backup.tar db/data/ sshd/host_keys

# restore
sudo tar --same-owner -xvf backup.tar
```