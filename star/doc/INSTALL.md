# INSTALL
> Ubuntu 16.04

## Enviornment
```
$ cat <(echo "OS:     " `lsb_release -d | cut -f2`) <(echo "Kernel: " `uname -a | cut -d' ' -f1,3,14`) <(docker --version) <(docker-compose --version)
OS:      Ubuntu 16.04.6 LTS
Kernel:  Linux 4.15.0-48-generic x86_64
Docker version 18.09.5, build e8ff056
docker-compose version 1.24.0, build 0aa59064
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
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
$ sudo apt update
$ sudo apt install -y docker-ce

$ sudo usermod -aG docker $USER
# logout & login
$ docker --version

$ sudo nano /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

### docker-compose
```
$ sudo apt install jq

$ nano ~/Downloads/install-docker-compose.sh
#!/bin/bash
compose_version=$(curl https://api.github.com/repos/docker/compose/releases/latest | jq .name -r)
output='/usr/local/bin/docker-compose'
curl -L https://github.com/docker/compose/releases/download/$compose_version/docker-compose-$(uname -s)-$(uname -m) -o $output
chmod +x $output
echo $(docker-compose --version)

$ chmod +x ~/Downloads/install-docker-compose.sh
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
> /dev/disk/by-uuid/2C3CBAA60F5CE503 /media/data auto nosuid,nodev,nofail,x-gvfs-show 0 0

sudo mkdir /media/data
sudo mount -a
```

## UFW
```
sudo ufw default deny

sudo ufw allow from 140.116.164.128/27 to any port 22019    # ssh
sudo ufw allow from 10.27.164.151/32 to any port 22019      # ssh for RPi
sudo ufw allow from 10.27.164.153/32 to any port 22019      # ssh for edge
sudo ufw allow from 140.116.221.10/32 to any port 22019     # ssh for VPN
sudo ufw allow from 0.0.0.0/0 to any port 5938              # teamviewer (accept exclusively)

# drop icmp (allow ping)
sudo sed -i '/ufw-before-input.*icmp/s/ACCEPT/DROP/g' /etc/ufw/before.rules

$ sudo nano /etc/ufw/before.rules
# add ↓ above ufw-before-input.*icmp
-A ufw-before-input -s 140.116.164.128/27 -p icmp --icmp-type echo-request -j ACCEPT
-A ufw-before-input -s 140.116.221.10/32  -p icmp --icmp-type echo-request -j ACCEPT

sudo ufw enable
sudo service ufw restart
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
$ sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/10-help-text
$ sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/91-release-upgrade
$ sudo nano /etc/update-motd.d/10-help-text
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