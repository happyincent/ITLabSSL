FROM alpine:3.9
# FROM alpine:latest
MAINTAINER  ddl <itlab.ee.ncku.edu.tw>

# Install packages
RUN apk add --update --no-cache \
    openssh \
    inotify-tools \
    supervisor \
    bash \
    logrotate

# Cleanup
RUN rm -rf /var/cache/* /tmp/*