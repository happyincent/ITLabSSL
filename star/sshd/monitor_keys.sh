#!/bin/bash

inotifywait -q -m -e close_write /home/${USERNAME}/.ssh/authorized_keys --format %e |
while read event; do
    echo `date '+%Y-%m-%d %H:%M:%S'`:authorized_keys:$event

    IFS=',' read -r -a KEYS <<< `ssh-keygen -lf /home/${USERNAME}/.ssh/authorized_keys | cut -d':' -f2 | cut -d' ' -f1 | paste -s -d ','`

    declare -i lineno=0
    while read -r line; do
        KEY=`echo $line | awk -F':' '{print $1}' | tr -d "\r\n"`
        PID=`echo $line | awk -F':' '{print $NF}' | tr -d "\r\n"`
        let ++lineno
        if [[ ! " ${KEYS[*]} " == *"$KEY"* ]]; then
            echo `date '+%Y-%m-%d %H:%M:%S'`:PID=$PID:disconnected \(killed\) | tee -a /var/log/monitor_sshd.log
            kill $PID
            sed -i "$lineno d" ${SSHD_ONLINE_LOG}
            ((lineno -= 1))
            sleep 1
        fi
    done < ${SSHD_ONLINE_LOG}

done