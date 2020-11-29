# star-swarm
Mange and Deploy services to the edge nodes with Docker Swarm.

## Installation

Manager: [Install X302LJ](/doc/INSTALL.md), [Install Docker (test)](/doc/DOCKER.md), [Install Buildx](/doc/BUILDX.md)

Worker (Edge Node): [Install Docker](/doc/INSTALL-worker.md)

---

## Build and Push images
```
docker buildx rm mybuilder
docker buildx create --name mybuilder --platform linux/amd64,linux/arm64,linux/arm/v7
docker buildx use mybuilder
docker buildx inspect --bootstrap # check platforms

docker login # login docker hub

cd image/
docker buildx bake
```

---

## Swarm Setup
### Manager
```
# sudo iptables -A INPUT -p tcp --dport 7777 -j ACCEPT
docker swarm leave --force
docker swarm init --advertise-addr 140.116.164.139:7777 --listen-addr 0.0.0.0:7777 --task-history-limit 0

# show ${WORKER_TOKEN}
docker swarm join-token worker
```

### Worker (Edge Node)
```
# Setup a "unique" hostname (NODE_NAME)
echo "127.0.0.1 ${NODE_NAME}" | sudo tee -a /etc/hosts
sudo hostnamectl set-hostname ${NODE_NAME}
docker info | grep Name # if not changed: sudo systemctl restart docker

# Join Swarm
docker swarm leave --force
docker swarm join --token ${WORKER_TOKEN} 140.116.164.139:7777
```

---

## Swarm Deployment

### Manager
```
docker stack deploy --prune --resolve-image always -c <(docker-compose -f star-manager.yml config) manager
```
> visualizer: visualize the swarm status

> live555proxy: proxy from `rtsp://root:xxxxx@10.27.164.152/live3.sdp` (max connections: 10) to `rtsp://store.itlab.ee.ncku.edu.tw:50001/proxyStream`

> [Manager's iptables](/doc/IPTABLES.md)

### Worker
#### 1. Edit `.env` (First time)
```
#### Edge Service Parameters ####
SSH_USER=limited-user
SSH_PORT=62422
SSH_NETLOC=ssl.itlab.ee.ncku.edu.tw

RTMP_REMOTE_NETLOC=nginx-rtmp:1935
RTMP_PATH=/itlab/

WS_REMOTE_NETLOC=web:8001
WS_PATH=/ws/edge/device/

RTMP_NETLOC=localhost:65000
WS_NETLOC=localhost:65001
```

#### 2. Deploy services: Autossh, Edge, FFmpeg
```
# Check Edge Nodes' JSON configs first
./node/generate.sh `ls $PWD/node/profile/*.json`

# deploy services
docker stack deploy --prune --resolve-image always -c <(docker-compose -f node/autossh.yml config) star0
docker stack deploy --prune --resolve-image always -c <(docker-compose `ls node/yml/*ffmpeg.yml | sed 's/^/-f /'` config) star1
docker stack deploy --prune --resolve-image always -c <(docker-compose `ls node/yml/*edge.yml | sed 's/^/-f /'` config) star2
```

#### 3. Add public keys to the website (First time)
```
# if new node join and not running autossh automatically:
# docker service update star0_autossh

docker service logs -f star0_autossh
```

---

## Add New Edge Node (JSON Config)
```
# Check NODE_NAME (HOSTNAME)
docker node ls

# Add JSON config in node/profile/${NODE_NAME}.json, an example format: 
{
    "NODE_NAME": "VM0",
    "DEVICES": [
        {
        "id": "VM0_1",
        "token": "8c368d73-e351-4e2e-9cab-d9f25710de2a",
        "postinfo_timetout": "10",
        "serial_baud": "9600",
        "serial_port": "",
        "rtsp_uri": ""
        },
        ...
    ]
}

## TX2 - Real Serial Port, Real IP Camera
"serial_port": "/dev/ttyACM0"
"rtsp_uri": "rtsp://root:xxxxx@10.27.164.152/live3.sdp"

## VM0 - Leave Serail blanking, Use RTSP Proxy
sed -i 's|"rtsp_uri": ""|"rtsp_uri": "rtsp://store.itlab.ee.ncku.edu.tw:50001/proxyStream"|g' node/profile/VM0.json
```

---

## Upgrading workers
### Update profiles or base YML
1. Generate config again
2. Deploy the specifc stack services again

### Update Dockerfile
1. Bake (build and push) again

2. Update or Deploy services again
  * autossh (star0), ffmpeg (star1)
    * Deploy the stack services again
  * edge (star2):
    * Force restart all services in `star2`
    * `docker service ls -q -f name='star2' | xargs -P10 -I{} docker service update -d --force {}`

---

## Other
### CMDs
```
# List stacks
docker stack ls

# Check service status
docker stack ps star0 (star1, star2)

# Check specific container's log
docker service logs -f star2_TX2_TX2_1-edge

# Remove all services
docker stack rm star0 star1 star2

# Force restart all VM's ffmpeg services
docker service ls -q -f name='star1_VM' | xargs -P10 -I{} docker service update -d --force {}

# Force stop all VM's ffmpeg services
docker service ls -q -f name='star1_VM' | xargs -P10 -I{} docker service scale -d {}=0

# Restart manager services
docker service update --force `docker service ls -q -f name='manager_live555proxy'`
docker service update --force `docker service ls -q -f name='manager_visualizer'`
```

### For Edge using DHCP
```
# Modify delay to 30s to wait DHCP (network-online) at startup 
sudo sed -i.bak 's/RestartSec=.*/RestartSec=30/' /lib/systemd/system/docker.service
```