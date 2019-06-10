FROM alpine:3.9
MAINTAINER  ddl <itlab.ee.ncku.edu.tw>
# Mod: https://github.com/Hermsi1337/docker-sshd

ARG         USERNAME=limited-user
ARG         PORT=22
ARG         MAX_SESSIONS=200

##############################

# Add user
RUN         adduser -h /home/${USERNAME} -s /bin/false -D ${USERNAME} && \ 
            sed -i "s/${USERNAME}:!/${USERNAME}:*/" /etc/shadow && \
            mkdir /home/${USERNAME}/.ssh

# Install latest SSHD
RUN         apk add --update --no-cache openssh

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

# Add keys folder
RUN         mkdir /host_keys