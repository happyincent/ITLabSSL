#!/bin/bash
cd ~/Desktop/

echo Stop all Docker containers ...
time docker-compose -f star/docker-compose.yml down &> /dev/null && echo -e "\nOK\n"

echo Backup star project ...
time sudo tar -zcpf star.tar.gz star/ && echo -e "\nOK\n"

echo Backup Docker images ...
time docker images -f "reference=*:star" --format "{{.Repository}}:{{.Tag}}" | xargs -P7 -I{} sh -c "docker save {} | gzip > {}.tar.gz" && echo -e "\nOK\n"

echo List tar files ...
du -h star.tar.gz *:star.tar.gz
