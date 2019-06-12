#!/bin/bash

tail -Fn0 ${SSHD_LOG} |
while read event; do

    case "$event" in 
        *Accepted\ publickey*)
            KEY=`echo $event | awk -F':' '{print $NF}' | tr -d "\r\n"` >> ${SSHD_ONLINE_LOG}
        ;;
        *User\ child*)
            PID=`echo $event | awk '{print $NF}'`
            [[ ! -z "$KEY" ]] && echo "$KEY:$PID" >> ${SSHD_ONLINE_LOG}
            echo `date '+%Y-%m-%d %H:%M:%S'`:PID=$PID:connected
        ;;
        *Disconnected\ from\ user*)
            echo `date '+%Y-%m-%d %H:%M:%S'`:disconnected
            
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
        ;;
    esac

done