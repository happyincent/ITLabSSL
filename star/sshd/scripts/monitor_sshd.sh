#!/bin/bash

tail -Fn0 ${SSHD_LOG} |
while read event; do

    case "$event" in 
        *Accepted\ publickey*)
            KEY=`echo $event | awk -F':' '{print $NF}' | tr -d "\r\n"`
        ;;
        *User\ child*)
            PID=`echo $event | awk '{print $NF}'`
            [[ ! -z "$KEY" ]] && echo "$KEY:$PID" >> ${SSHD_ONLINE_LOG}
            echo `date '+%Y-%m-%d %H:%M:%S'`:PID=$PID:connected
        ;;
        *Disconnected\ from\ user*)
            bash /check_online.sh
        ;;
    esac

done