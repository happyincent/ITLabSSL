# iptables-persistent

```
# sudo apt install iptables-persistent

sudo iptables -I DOCKER-USER -p tcp -m multiport --dports 50000,50001 -j DROP

sudo iptables -I DOCKER-USER -s 140.116.164.128/27 -p tcp -m multiport --dports 50000,50001 -j RETURN
sudo iptables -I DOCKER-USER -s 10.27.164.128/27 -p tcp -m multiport --dports 50000,50001 -j RETURN
sudo iptables -I DOCKER-USER -s 120.114.234.117/32 -p tcp -m multiport --dports 50000,50001 -j RETURN

sudo iptables -L DOCKER-USER -n --line-numbers

sudo dpkg-reconfigure iptables-persistent
```