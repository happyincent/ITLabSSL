# INSTALL Worker
> Install docker in TX2, RPi, VM (Debian Based)

## Docker
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

sudo mkdir -p /etc/docker/
sudo nano /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}

sudo systemctl restart docker
```

## [Docker Compose (single)](https://withblue.ink/2019/07/13/yes-you-can-run-docker-on-raspbian.html)
```
sudo apt update
sudo apt install -y python python-pip libffi-dev python-backports.ssl-match-hostname

pip install docker-compose

source ~/.profile
docker-compose version
```