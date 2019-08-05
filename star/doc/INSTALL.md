# INSTALL
> Ubuntu 16.04

## Enviornment
```
$ cat <(echo "OS:     " `lsb_release -d | cut -f2`) <(echo "Kernel: " `uname -a | cut -d' ' -f1,3,14`) <(docker --version) <(docker-compose --version)
OS:      Ubuntu 18.04.2 LTS
Kernel:  Linux 4.18.0-25-generic x86_64
Docker version 19.03.0, build aeac949
docker-compose version 1.24.1, build 4667896
```

## APT Install
```
sudo apt update
sudo apt install curl

# hime (http://goodjack.blogspot.com/2013/08/linux-phonetic-setting.html)
sudo apt install hime

# vlc
sudo apt purge parole
sudo apt install vlc

# vscode
curl -o code.deb -L http://go.microsoft.com/fwlink/?LinkID=760868
sudo apt install ./code.deb
```

### docker
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

### docker-compose
```
sudo apt install jq

nano ~/Downloads/install-docker-compose.sh
#!/bin/bash
compose_version=$(curl https://api.github.com/repos/docker/compose/releases/latest | jq .name -r)
output='/usr/local/bin/docker-compose'
curl -L https://github.com/docker/compose/releases/download/$compose_version/docker-compose-$(uname -s)-$(uname -m) -o $output
chmod +x $output
echo $(docker-compose --version)

chmod +x ~/Downloads/install-docker-compose.sh
sudo ~/Downloads/install-docker-compose.sh
```

## Mount disk
```
# GUI
sudo apt install gnome-disk-utility

# Command line
ls -l /dev/disk/by-uuid/
lsblk # sudo fdisk -l

sudo nano /etc/fstab
> /dev/disk/by-uuid/e7908ed5-67fd-4079-a23a-6ef417133e23 /media/data auto nosuid,nodev,nofail,x-gvfs-show 0 0

sudo mkdir /media/data
sudo mount -a
```

## iptables
```
# Note: Docker daemon will add rules to allow all Docker services by default.

# Ping
sudo iptables -A INPUT -s 140.116.164.128/27 -p icmp --icmp-type echo-request -j ACCEPT
sudo iptables -A INPUT -s 140.116.215.192/28 -p icmp --icmp-type echo-request -j ACCEPT
sudo iptables -A INPUT -s 140.116.221.10/32 -p icmp --icmp-type echo-request -j ACCEPT

# SSH
sudo iptables -A INPUT -s 140.116.164.128/27 -p tcp --dport 22019 -j ACCEPT
sudo iptables -A INPUT -s 140.116.215.192/28 -p tcp --dport 22019 -j ACCEPT
sudo iptables -A INPUT -s 140.116.221.10/32 -p tcp --dport 22019 -j ACCEPT

# TeamViewer
sudo iptables -A INPUT -s 140.116.164.128/27 -p tcp --dport 5938 -j ACCEPT
sudo iptables -A INPUT -s 140.116.215.192/28 -p tcp --dport 5938 -j ACCEPT
sudo iptables -A INPUT -s 140.116.221.10/32 -p tcp --dport 5938 -j ACCEPT

# Accept localhost, exist & related packets
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

# Drop other packet (make sure SSH has been accepted !!)
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP

# Save rules
sudo dpkg-reconfigure iptables-persistent
```

## Install opensssh-server
```
sudo apt install openssh-server -y
sudo update-rc.d -f ssh remove
sudo update-rc.d -f ssh defaults
cd /etc/ssh/
sudo mkdir insecure_original_default_keys
sudo mv ssh_host_* insecure_original_default_keys/
sudo dpkg-reconfigure openssh-server

sudo sed -i \
         -e 's|Port [0-9]*|Port 22019|' \
         -e 's|#PasswordAuthentication yes|PasswordAuthentication no|' \
         /etc/ssh/sshd_config

sudo service ssh restart

ssh-keygen -t rsa

touch ~/.ssh/authorized_keys
chmod 640 ~/.ssh/authorized_keys
```

## Install TeamViewer without a connected monitor
https://gist.github.com/happyincent/c5c56a73ff35212a3bf0af365b03daee


## Change welcome message
```
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/10-help-text
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/50-motd-news
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/80-livepatch
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/91-release-upgrade
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/95-hwe-eol
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/98-fsck-at-reboot

sudo nano /etc/update-motd.d/10-help-text

printf "  _____ _______ _           _\n"
printf " |_   _|__   __| |         | |\n"
printf "   | |    | |  | |     __ _| |__\n"
printf "   | |    | |  | |    / _  |  _ \ \n"
printf "  _| |_   | |  | |___| (_| | |_) |\n"
printf " |_____|  |_|  |______\____|____/\n"
```


## Install Cuda 9.2 (optional)

### nvidia driver
```
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
sudo apt-mark hold nvidia-396
sudo apt install nvidia-396 nvidia-modprobe
```

### cuda
```
curl -o cuda_9.2.148_396.37_linux.run -L https://developer.nvidia.com/compute/cuda/9.2/Prod2/local_installers/cuda_9.2.148_396.37_linux
chmod +x cuda_9.2.148_396.37_linux.run
./cuda_9.2.148_396.37_linux.run --extract=$HOME
sudo ./cuda-linux.9.2.148-24330188.run
sudo ./cuda-samples.9.2.148-24330188-linux.run

sudo bash -c "echo /usr/local/cuda/lib64/ > /etc/ld.so.conf.d/cuda.conf"
sudo ldconfig

sudo sed -i 's|"$|:/usr/local/cuda/bin"|' /etc/environment

# test samples
cd /usr/local/cuda/samples/
sudo make
cd /usr/local/cuda/samples/bin/x86_64/linux/release/
./deviceQuery

# remove installer files
rm -i ~/cuda* ~/NVIDIA-Linux-x86_64-396.37.run
```

### cudnn
```
# In https://developer.nvidia.com/rdp/cudnn-download, download the following files

cd ~/Downloads
sudo dpkg -i libcudnn7_7.4.2.24-1+cuda9.2_amd64.deb
sudo dpkg -i libcudnn7-dev_7.4.2.24-1+cuda9.2_amd64.deb
sudo dpkg -i libcudnn7-doc_7.4.2.24-1+cuda9.2_amd64.deb

echo 'export LD_LIBRARY_PATH="LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+${LD_LIBRARY_PATH}:}/usr/local/cuda/extras/CUPTI/lib64"' >> ~/.bashrc
source ~/.bashrc

# test samples
cp -r /usr/src/cudnn_samples_v7/ ~/Downloads/
cd ~/Downloads/cudnn_samples_v7/mnistCUDNN/
make clean && make
./mnistCUDNN

# remove installer files
rm -rf ~/Downloads/cudnn_samples_v7/ ~/Downloads/libcudnn7*
```

https://medium.com/@zhanwenchen/install-cuda-9-2-and-cudnn-7-1-for-tensorflow-pytorch-gpu-on-ubuntu-16-04-1822ab4b2421