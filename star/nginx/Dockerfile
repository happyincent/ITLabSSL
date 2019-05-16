FROM alpine:3.9
MAINTAINER ddl <itlab.ee.ncku.edu.tw>

ENV NGINX_VERSION=1.16.0
ENV TZ=Asia/Taipei

ENV MAKEFLAGS="-j16"

###############################
# Install packages
RUN apk add --update --no-cache \
    nano logrotate

# Setup scripts
COPY crontab /crontab
COPY run.sh /run.sh
RUN chmod 775 /run.sh
RUN find /etc/periodic/ -type f -exec rm {} \;

# Setup timezone
RUN apk add --update --no-cache tzdata && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    date && \
    apk del tzdata

###############################

# Get nginx source
RUN cd /tmp && \
  wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && \
  tar zxf nginx-${NGINX_VERSION}.tar.gz && \
  rm nginx-${NGINX_VERSION}.tar.gz

# Build dependencies
RUN apk add --update --no-cache \
  build-base \
  ca-certificates \
  curl \
  gcc \
  libc-dev \
  libgcc \
  linux-headers \
  make \
  musl-dev \
  openssl \
  openssl-dev \
  pcre \
  pcre-dev \
  pkgconf \
  pkgconfig \
  zlib-dev

# Compile nginx with nginx-rtmp module
RUN cd /tmp/nginx-${NGINX_VERSION} && \
  ./configure \
  --prefix=/opt/nginx \
  --with-http_ssl_module \
  --with-http_v2_module \
  --with-http_auth_request_module \
  --with-threads \
  --with-file-aio \
  --with-debug \
  --conf-path=/opt/nginx/nginx.conf \
  && \
  cd /tmp/nginx-${NGINX_VERSION} && make && make install

# Cleanup
RUN rm -rf /var/cache/* /tmp/*

# Setup PATH
ENV PATH "/opt/nginx/sbin:${PATH}"