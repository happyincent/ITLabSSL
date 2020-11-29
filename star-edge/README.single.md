# star-edge
> Deploy services to a single edge nodes with Docker Compose.

## Installation

Worker (Edge Node): [Install Docker](/doc/INSTALL-worker.md)

## Usage

### 1. Edit `.env` `star-single.env` (First time)
#### .env
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

#### star-single.env
```
#### Device Parameters ####
ID=TMP
TOKEN=7b5f50e1-9c8d-4d6b-a321-2f1563572fb1
POSTINFO_TIMEOUT=10
SERIAL_BAUD=9600
SERIAL_PORT=/dev/ttyACM0
RTSP_URI=rtsp://root:xxxxx@10.27.164.152/live3.sdp
```

#### 1.1 Create symbolic path of here
```
sudo ln -s `pwd` /var/star-edge
```
> (OLD) 1.1 Check SERIAL_PORT is in the pair of `star-single.yml` - `devices`

### 2. Build and Run
```
sudo `which docker-compose` -f star-single.yml build
docker-compose -f star-single.yml up -d
```

#### 3. Add Public key to the website (First time)
```
docker-compose -f star-single.yml logs -f autossh # cat ./image/autossh/keys/id_rsa.pub
```

#### Reset Token
```
docker-compose rm -f -s -v edge ffmpeg
# Modify "TOKEN" in star-single.env
docker-compose -f star-single.yml up -d
```

#### Remove containers & images
```
docker-compose -f star-single.yml down
docker rmi autossh:starE ffmpeg:starE edge:starE
```