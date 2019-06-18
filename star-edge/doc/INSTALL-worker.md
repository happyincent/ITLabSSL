# INSTALL Worker
> Install docker in TX2, RPi, VM (Debian Based)

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