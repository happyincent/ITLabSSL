FROM alpine:3.9
MAINTAINER  ddl <itlab.ee.ncku.edu.tw>
# Mod: https://github.com/Hermsi1337/docker-sshd

ENV         USERNAME=limited-user
# ENV         OPENSSH_VERSION=7.9_p1-r5
ENV         PORT=22
ENV         MAX_SESSIONS=200

##############################

# Add user
RUN         adduser -h /home/${USERNAME} -s /bin/false -D ${USERNAME} && \ 
            sed -i "s/${USERNAME}:!/${USERNAME}:*/" /etc/shadow && \
            mkdir /home/${USERNAME}/.ssh

# Install SSHD
RUN         apk add --update --no-cache openssh
# RUN         apk add --update --no-cache openssh=${OPENSSH_VERSION}

RUN         sed -i "s|#Port [0-9]*|Port ${PORT}|" /etc/ssh/sshd_config
RUN         sed -i "s|#MaxSessions [0-9]*|MaxSessions ${MAX_SESSIONS}|" /etc/ssh/sshd_config
RUN         echo -e "\n\
Match User ${USERNAME}\n\
    PasswordAuthentication no\n\
    AllowAgentForwarding no\n\
    AllowTcpForwarding yes\n\
    PermitOpen nginx-rtmp:1935 web:8001\n\
    ForceCommand echo 'This account can only be used for tunneling'" \
            >> /etc/ssh/sshd_config

# Cleanup
RUN rm -rf /var/cache/* /tmp/*

# Setup config
COPY        run.sh /run.sh
RUN         chmod 775 /run.sh
RUN         mkdir /host_keys