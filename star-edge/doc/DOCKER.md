# INSTALL Docker

## Docker 19.03+ (test builds)
```
curl -fsSL https://test.docker.com -o test-docker.sh
sudo sh test-docker.sh
sudo usermod -aG docker $USER
```

## Docker Compose
```
pip install docker-compose
nano .profile
> PATH="$HOME/.local/bin:$PATH"
```

## [Install Buildx](https://github.com/docker/buildx/issues/57)
```
# install qemu in static mode (without `binfmt-support`)
sudo apt install qemu qemu-user-static binfmt-support-

# install binfmt config files
git clone https://github.com/computermouth/qemu-static-conf.git
sudo mkdir -p /lib/binfmt.d
sudo cp qemu-static-conf/qemu-{aarch64,arm}-static.conf  /etc/binfmt.d
#  or enable more emulated architectures:
# sudo cp qemu-static-conf/*.conf /lib/binfmt.d/

sudo systemctl restart systemd-binfmt.service

git clone git://github.com/docker/buildx && cd buildx
make install
```