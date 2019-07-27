#!/bin/bash
DIR=/home/itlab/Desktop/star
BACKUP_DIR=/home/itlab/Desktop/backup-`date +"%Y%m%d"`

mkdir -p $BACKUP_DIR

echo Stop all Docker containers ...
time sudo docker-compose -f $DIR/docker-compose.yml down &> /dev/null && echo -e "\nOK\n"

echo Backup star project ...
time sudo tar -zcpf $BACKUP_DIR/star.tar.gz -C `dirname $DIR` ./`basename $DIR` && echo -e "\nOK\n"

echo Backup Docker images ...
time docker images -f "reference=*:star" --format "{{.Repository}}:{{.Tag}}" | \
     xargs -P7 -I{} sh -c "sudo docker save {} | gzip > $BACKUP_DIR/{}.tar.gz" && \
     echo -e "\nOK\n"

echo List tar files ...
du -h $BACKUP_DIR/star.tar.gz $BACKUP_DIR/*:star.tar.gz
