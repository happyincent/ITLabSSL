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
source .profile
```