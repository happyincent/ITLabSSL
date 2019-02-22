FROM alpine:3.9
MAINTAINER  ddl <itlab.ee.ncku.edu.tw>

ENV         USERNAME=limited-user
ENV         OPENSSH_VERSION=7.9_p1-r2
ENV         PORT=62422

# Mod: https://github.com/Hermsi1337/docker-sshd

##############################

# Add user
RUN         adduser -h /home/${USERNAME} -s /bin/false -D ${USERNAME} && \ 
            sed -i "s/${USERNAME}:!/${USERNAME}:*/" /etc/shadow && \
            mkdir /home/${USERNAME}/.ssh

# Install SSHD
RUN         apk add --update --no-cache openssh=${OPENSSH_VERSION} && \
            rm -rf /var/cache/apk/* /tmp/*

RUN         sed -i "s|#Port [0-9]*|Port ${PORT}|" /etc/ssh/sshd_config
RUN         echo -e "\n\
Match User ${USERNAME}\n\
    PasswordAuthentication no\n\
    AllowAgentForwarding no\n\
    AllowTcpForwarding yes\n\
    PermitOpen nginx:1935 web:8000 web:8001\n\
    ForceCommand echo 'This account can only be used for tunneling'" \
            >> /etc/ssh/sshd_config

# Setup config
COPY        run.sh /run.sh
RUN         chmod 775 /run.sh
RUN         mkdir /host_keys