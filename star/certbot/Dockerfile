# FROM docker:18.09.6
FROM docker:latest
MAINTAINER ddl <itlab.ee.ncku.edu.tw>

# Install packages for certbot
# https://hub.docker.com/r/certbot/certbot/dockerfile
RUN apk add --update --no-cache --virtual .certbot-deps \
    libffi \
    libssl1.1 \
    openssl \
    ca-certificates \
    binutils

# Install packages for date -d, for start.sh, certbot
RUN apk add --update --no-cache \
    coreutils \
    bash \
    certbot

# Cleanup
RUN rm -rf /var/cache/* /tmp/*

# Setup ENTRYPOINT
ADD start.sh /bin/start.sh
RUN chmod +x /bin/start.sh
ENTRYPOINT [ "/bin/start.sh" ]