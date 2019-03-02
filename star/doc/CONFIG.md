# Config

## docker-compose.yml

### volumnes
* db
  * `./db/data` : storage for MongoDB
* redis
  * `./redis/data` : storage for redis
* web
  * `./web/app` : root path of django **(web & nginx)**
  * `./web/supervisord.conf` : supervisord config file 
  * `./web/logrotate.conf` : logrotate config file
  * `./web/crontab` : crond config file
  * `./web/run.sh` : startup script for the container 
  * `./sshd/authorized_keys` : file with client's public key **(web & sshd)**
  * `./log/web/` : log file for crond, daphne, gunicorn, supervisord
  * `/media/data/record` : [nginx.conf](../nginx/nginx.conf) - record_path **(web & nginx)** **(mount disk)**

* nginx
  * `./nginx/nginx_init.conf` : nginx config file for the first time
  * `./nginx/nginx.conf` : nginx config file
  * `./nginx/logrotate.conf` : logrotate config file
  * `./nginx/crontab` : crond config file
  * `./nginx/run.sh` : startup script for the container 
  * `./web/app` : root path of django **(web & nginx)**
  * `./log/nginx/` : log file for access, rtmp_access, error
  * `/tmp/key` : [nginx.conf](../nginx/nginx.conf) - hls_key_path
  * `/media/data/record` : [nginx.conf](../nginx/nginx.conf) - record_path  **(web & nginx)** **(mount disk)**
  * `/etc/letsencrypt` : path for https key files **(nginx & letsencrypt)**
  * `./letsencrypt/letsencrypt-www` : temporary path for letsencrypt **(nginx & letsencrypt)**
* letsencrypt
  * `./letsencrypt/letsencrypt-www` : temporary path for letsencrypt **(nginx & letsencrypt)**
  * `/etc/letsencrypt` : path for https key files **(nginx & letsencrypt)**
  * `/var/run/docker.sock` : restart nginx container after renew certificate **(letsencrypt & host)**
* sshd
  * `./sshd/host_keys` : path for sshd server's key files
  * `./sshd/authorized_keys` : file with client's public key **(web & sshd)**
    * `/home/limited-user/.ssh/authorized_keys` : path in container
      * ssh server's username=limited-user

### command
* redis
  * `redis-server --appendonly yes` : redis AOF (for persistence, fsync every second)
* web
  * `sh -c "/run.sh"` : run [run.sh](../web/run.sh)
* nginx
  * `sh -c "/run.sh"` : run [run.sh](../nginx/run.sh)
* sshd
  * `sh -c "/run.sh"` : run [run.sh](../sshd/run.sh)

> make sure all run.sh files have the execution permission (`chmod +x`)

### ports
* nginx
  * `80` : http port for letsencrypt
  * `443` : https port
* sshd
  * `62422` : ssh port for clients (TX2)

### depends_on
* port depend
  * web
    * db:27017, redis:6379
  * nginx
    * web:8000, web:8001
  * sshd
    * nginx:1935, web:8001
* startup order
  * db & redis -> web -> nginx -> sshd, letsencrypt

---

## nginx
* Dockerfile
  * compile nginx with rtmp module, ffmpeg
  * `TZ` : timezone
  * `/opt/nginx` : path to nginx files

* crontab
  * rotate log every one hour (xx:59)

* nginx.conf
  * rtmp (port 1935)
    * `http://web:8000/hooks/on_publish` : rtmp hook to web (django)
    * `/media/data/record` : vod path
    * `/tmp/key` : hls key path
    * `https://ssl.itlab.ee.ncku.edu.tw/key/` : hls key url
  
  * http (port 80, 443)
    * `ssl.itlab.ee.ncku.edu.tw` : server domain name
    * `/tmp/letsencrypt` : temporary path for letsencrypt
    * `/static/` : path to static files (`/www/static/`)
    * `/media/data/record` : vod path
    * `auth_request /check_user` : auth user by [django](../web/app/home/urls.py)
    * `/etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/` : path for https key files

* [run.sh](../nginx/run.sh)
  * `/etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/dhparam.pem` : path to the DH key

---

## web
* Dockerfile
  * `TZ` : timezone
  * `https://ssl.itlab.ee.ncku.edu.tw/` : full URL location

* crontab
  * rotate log every one hour (xx:59)
  * check django's cron jobs every 15 minutes
    * log stdout and stderr to `/var/log/cron.log`

* supervisord.conf
  * log path : `/var/log/supervisord.log`, `/var/log/gunicorn.log`, `/var/log/daphne.log`
  * gunicorn : port 8000
  * daphne : port 8001

* [`app/star/settings.py`](../web/app/star/settings.py)
  * DATABASES : MongoDB with hostname `db` and port `27017`
  * CACHES, CHANNEL_LAYERS : redis with hostname `redis` and port `6379`
  * Other Configs
    ```
    # SMTP
    EMAIL_XXX=YYY
    ...
    HLS_URL = 'https://ssl.itlab.ee.ncku.edu.tw/hls/'
    SSH_KEY_PATH = '/authorized_keys'
    VOD_URL = 'https://ssl.itlab.ee.ncku.edu.tw/vod/'
    VOD_DIR = '/media/data/record'
    ```

---

## sshd
* Dockerfile
  * `USERNAME=limited-user` : server's username for clients (TX2)
  * `PORT=62422` : ssh port for clients (TX2)
  * `PermitOpen nginx:1935 web:8001` : only forward these local ports
* [run.sh](../sshd/run.sh)
  * `/home/limited-user/.ssh/authorized_keys` : file with client's public key
    * ssh server's username=limited-user