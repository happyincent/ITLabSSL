#!/bin/bash
DIR=/home/itlab/Desktop/star
BACKUP_DIR=`ls -d /home/itlab/Desktop/backup*[0-9] | sort -n | tail -n1`

echo Remove star project ...
sudo rm -rf $DIR && echo -e "OK\n"

echo Remove Docker images ...
sudo docker rmi -f $(docker images -q -f "reference=*:star") &> /dev/null && echo -e "OK\n"

echo Restore star project ...
time sudo tar --same-owner -zxpf $BACKUP_DIR/star.tar.gz -C `dirname $DIR` && echo -e "\nOK\n"

echo Restore Docker images ...
time ls $BACKUP_DIR/*:star.tar.gz | xargs -P7 -I{} sh -c "gunzip -c {} | sudo docker load" &> /dev/null && echo -e "\nOK\n"

echo Start all Docker containers ...
time sudo docker-compose -f $DIR/docker-compose.yml up -d &> /dev/null && echo -e "\nOK"
