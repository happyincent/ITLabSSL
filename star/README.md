# StarTech

## Enviornment

```
$ cat <(echo "OS:     " `lsb_release -d | cut -f2`) <(echo "Kernel: " `uname -a | cut -d' ' -f1,3,14`) <(docker --version) <(docker-compose --version)
OS:      Ubuntu 16.04.5 LTS
Kernel:  Linux 4.15.0-39-generic x86_64
Docker version 18.09.0, build 4d60db4
docker-compose version 1.22.0, build f46880fe
```

## dockers

* DB
  * alpine-mongo
* web
  * python3-alpine
  * django --> gunicorn
* nginx
  * alpine

## exec
```
docker exec -it web-star gunicorn star.wsgi:application -c gunicorn.config.py

docker exec -it web-star python manage.py runserver 0.0.0.0:8000
```