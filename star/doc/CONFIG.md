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
  * `/tmp/hls` : [nginx.conf](../nginx-rtmp/nginx.conf) - hls_path
  * `/tmp/key` : [nginx.conf](../nginx-rtmp/nginx.conf) - hls_key_path
  * `/media/data/record` : [nginx.conf](../nginx/nginx.conf) - record_path  **(web & nginx)** **(mount disk)**
  * `/tmp/letsencrypt-www` : temporary path for letsencrypt **(nginx & certbot)**
  * `./certbot/letsencrypt/:/etc/letsencrypt/` : path for https key files **(nginx & certbot)**
  
* certbot
  * `/var/run/docker.sock` : restart nginx container after renew certificate **(certbot & host)**
  * `/tmp/letsencrypt-www` : temporary path for letsencrypt **(nginx & certbot)**
  * `./certbot/letsencrypt/:/etc/letsencrypt/` : path for https key files **(nginx & certbot)**

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
* nginx-rtmp
  * `sh -c "/run.sh"` : run [run.sh](../nginx-rtmp/run.sh)
* sshd
  * `sh -c "/run.sh"` : run [run.sh](../sshd/run.sh)

> make sure all run.sh files have the execution permission (`chmod +x`)

### ports
* nginx
  * `80` : http port for certbot
  * `443` : https port
* sshd
  * `62422` : ssh port for clients (edge)

### depends_on
* port depend
  * web
    * db:27017, redis:6379
  * nginx
    * web:8000, web:8001
  * sshd
    * nginx-rtmp:1935, web:8001
* startup order
  * db & redis -> web -> nginx / nginx-rtmp -> sshd, certbot

---

## nginx
* Dockerfile
  * compile nginx with rtmp module, ffmpeg
  * `TZ` : timezone
  * `/opt/nginx` : path to nginx files

* crontab
  * rotate log every one hour (xx:59)

* nginx.conf
  
  * http (port 80, 443)
    * `ssl.itlab.ee.ncku.edu.tw` : server domain name
    * `/tmp/letsencrypt` : temporary path for certbot
    * `/static/` : path to static files (`/www/static/`)
    * `/media/data/record` : vod path
    * `/tmp/hls` : hls m3u8, ts path
    * `/tmp/key` : hls key path
    * `auth_request /check_user` : auth user by [django](../web/app/home/urls.py)
    * `/etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/` : path for https key files

* [run.sh](../nginx/run.sh)
  * `/etc/letsencrypt/live/ssl.itlab.ee.ncku.edu.tw/dhparam.pem` : path to the DH key

---

## nginx-rtmp

* Dockerfile, crontab same as ngin

* nginx.conf
  * rtmp (port 1935)
    * `http://web:8000/hooks/on_publish` : rtmp hook to web (django)
    * `/media/data/record` : vod path
    * `/tmp/hls` : hls m3u8, ts path
    * `/tmp/key` : hls key path
    * `https://ssl.itlab.ee.ncku.edu.tw/key/` : hls key url
  
  * http (port 80)
    * `/control` : rtmp control (only between containers)

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
    SETUP_MSG => several configs required in star-edge's .env
    HLS_URL = 'https://ssl.itlab.ee.ncku.edu.tw/hls/'
    SSH_KEY_PATH = '/authorized_keys'
    VOD_URL = 'https://ssl.itlab.ee.ncku.edu.tw/vod/'
    VOD_DIR = '/media/data/record'
    ```

---

## sshd
* Dockerfile
  * `USERNAME=limited-user` : server's username for clients (edge)
  * `PORT=62422` : ssh port for clients (edge)
  * `MAX_SESSIONS=200` : maximum number of open sessions permitted per one IP
  * `PermitOpen nginx-rtmp:1935 web:8001` : only forward these local ports
* [run.sh](../sshd/run.sh)
  * `/home/limited-user/.ssh/authorized_keys` : file with client's public key
    * ssh server's username=limited-user
