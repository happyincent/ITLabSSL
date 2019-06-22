#!/bin/bash

tail -Fn0 ${SSHD_LOG} |
while read newline; do

    case "$newline" in 
        *Accepted\ publickey*)
            KEY=`echo $newline | awk -F':' '{print $NF}' | tr -d "\r\n"`
        ;;
        *User\ child*)
            PID=`echo $newline | awk '{print $NF}'`

            (
                flock -x 200

                [[ ! -z "$KEY" ]] && echo "$KEY:$PID" >> ${SSHD_ONLINE_LOG}
            
            ) 200> ${SSHD_ONLINE_LOG}.lock
            
            echo `date '+%Y-%m-%d %H:%M:%S'`:PID=$PID:connected
        ;;
        *Disconnected\ from\ user*)
            bash /check_online.sh &
        ;;
        *Closing\ connection*)
            bash /check_online.sh &
        ;;
    esac

done