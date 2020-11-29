#!/bin/bash

(
    flock -x 200

    IFS=',' read -r -a PIDS <<< `pgrep -x "sshd: ${USERNAME}" | paste -s -d ','`

    declare -i lineno=0
    while read -r line; do
        PID=`echo $line | awk -F':' '{print $NF}' | tr -d "\r\n"`
        let ++lineno
        if [[ ! " ${PIDS[*]} " == *"$PID"* ]]; then
            echo `date '+%Y-%m-%d %H:%M:%S'`:PID=$PID:disconnected
            sed -i "$lineno d" ${SSHD_ONLINE_LOG}
            ((lineno -= 1))
            sleep 1
        fi
    done < ${SSHD_ONLINE_LOG}

) 200> ${SSHD_ONLINE_LOG}.lock