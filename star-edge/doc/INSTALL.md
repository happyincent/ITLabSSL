# INSTALL
> Xubuntu 18.04 @ Asus X302LJ

## Environment
```
$ cat <(echo "OS:     " `lsb_release -d | cut -f2`) <(echo "Kernel: " `uname -a | cut -d' ' -f1,3,14`) <(docker --version) <(docker-compose --version) <(docker buildx version)
OS:      Ubuntu 18.04.2 LTS
Kernel:  Linux 4.18.0-20-generic x86_64
Docker version 19.03.0-beta4, build e4666ebe81
docker-compose version 1.24.0, build 0aa5906
github.com/docker/buildx v0.2.2-6-g2b03339 2b03339235021a481300385977ca5a70a403b7c0
```

## API Install
```
sudo apt update
sudo apt install curl git
sudo apt install iptables-persistent

# hime (http://goodjack.blogspot.com/2013/08/linux-phonetic-setting.html)
sudo apt install hime

# vscode
curl -o code.deb -L http://go.microsoft.com/fwlink/?LinkID=760868
sudo apt install ./code.deb
```

## Screen Resolution & Ignore LidSwitch
```
cvt 1920 1080 # Calculate mode lines
sudo xrandr --newmode "1920x1080_60.00"  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync
sudo xrandr --addmode eDP-1 "1920x1080_60.00"
# Apply the new resolution in the Display settings

$ nano ~/.profile
xrandr --newmode "1920x1080_60.00"  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync 2> /dev/null
xrandr --addmode eDP-1 "1920x1080_60.00" 2> /dev/null

echo 'HandleLidSwitch=ignore' | tee --append /etc/systemd/logind.conf
echo 'HandleLidSwitchDocked=ignore' | tee --append /etc/systemd/logind.conf
sudo service systemd-logind restart
```

## UFW
```
sudo ufw default deny

sudo ufw allow from 140.116.164.128/27 to any port 22019    # ssh
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
         -e 's|#Port 22|Port 22019|' \
         -e 's|#PasswordAuthentication yes|PasswordAuthentication no|' \
         /etc/ssh/sshd_config

sudo service ssh restart

ssh-keygen -t rsa

touch ~/.ssh/authorized_keys
chmod 640 ~/.ssh/authorized_keys
```

## Change welcome message
```
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/10-help-text
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/91-release-upgrade
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/80-livepatch
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/50-motd-news
sudo sed -i '/^#/! s/^/# /g' /etc/update-motd.d/95-hwe-eol

sudo nano /etc/update-motd.d/10-help-text
printf "  _____ _______ _           _\n"
printf " |_   _|__   __| |         | |\n"
printf "   | |    | |  | |     __ _| |__\n"
printf "   | |    | |  | |    / _  |  _ \ \n"
printf "  _| |_   | |  | |___| (_| | |_) |\n"
printf " |_____|  |_|  |______\____|____/\n"
```