FROM alpine:3.9
MAINTAINER  ddl <itlab.ee.ncku.edu.tw>

# Install packages
RUN apk add --update --no-cache \
    openssh \
    inotify-tools \
    supervisor \
    bash

# Cleanup
RUN rm -rf /var/cache/* /tmp/*