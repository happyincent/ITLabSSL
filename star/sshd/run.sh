#!/bin/sh

# add user if not exist
adduser -h /home/${USERNAME} -s /bin/false -D ${USERNAME} && \
    sed -i "s/${USERNAME}:!/${USERNAME}:*/" /etc/shadow && \
    mkdir /home/${USERNAME}/.ssh

# restore host keys or generate if not present
mkdir -p ${HOSTKEY_DIR}
cp ${HOSTKEY_DIR}/* /etc/ssh/
ssh-keygen -A
cp /etc/ssh/ssh_host_* ${HOSTKEY_DIR}

# setup files
mkdir -p "$(dirname "${SSHD_ONLINE_LOG}")" && cat /dev/null > ${SSHD_ONLINE_LOG}
touch ${SSHD_LOG}

# setup permission
chmod 644 ${SSHD_ONLINE_LOG}
chmod 644 /var/log/*.log
chmod 644 /home/${USERNAME}/.ssh/authorized_keys
chmod 644 /logrotate.conf
chown root:root /logrotate.conf

# load and start supervisord jobs
supervisord -c /etc/supervisord.conf
supervisorctl start all

# load crontab and start in foreground
cat /crontab > /var/spool/cron/crontabs/root
crond -b

# setup sshd_config
sed -i "s|#MaxSessions [0-9]*|MaxSessions 200|" /etc/ssh/sshd_config
sed -i "s|#LogLevel .*|LogLevel VERBOSE|" /etc/ssh/sshd_config

sed -i '/sftp/s/^/#/' /etc/ssh/sshd_config

echo -e "\n\
Match User ${USERNAME}\n\
    PasswordAuthentication no\n\
    AllowAgentForwarding no\n\
    AllowTcpForwarding yes\n\
    PermitOpen nginx-rtmp:1935 web:8001\n\
    ForceCommand echo This account can only be used for tunneling" \
            >> /etc/ssh/sshd_config

# run sshd in "not detach" mode, logging to sshd.log
/usr/sbin/sshd -D -E ${SSHD_LOG}