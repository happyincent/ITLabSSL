#!/bin/bash
cd ~/Desktop/

echo Remove star project ...
sudo rm -rf star/ && echo -e "OK\n"

echo Remove Docker images ...
docker rmi -f $(docker images -q -f "reference=*:star") &> /dev/null && echo -e "OK\n"

echo Restore star project ...
time sudo tar --same-owner -zxpf star.tar.gz && echo -e "\nOK\n"

echo Restore Docker images ...
time ls *:star.tar.gz | xargs -P7 -I{} sh -c "gunzip -c {} | docker load" &> /dev/null && echo -e "\nOK\n"

echo Start all Docker containers ...
time sudo docker-compose -f star/docker-compose.yml up -d &> /dev/null && echo -e "\nOK"
