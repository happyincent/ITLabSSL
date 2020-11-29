ARG NGINX_VERSION=1.16.0

ARG NGINX_PREFIX=/opt/nginx
ARG MAKEFLAGS="-j16"
ARG TZ=Asia/Taipei

###############################
FROM alpine:3.9 as build-nginx
ARG NGINX_VERSION
ARG NGINX_PREFIX
ARG MAKEFLAGS

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

# Compile nginx with modules
RUN cd /tmp/nginx-${NGINX_VERSION} && \
    ./configure \
    --prefix=${NGINX_PREFIX} \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-http_auth_request_module \
    --with-threads \
    --with-file-aio \
    --with-debug \
    --conf-path=${NGINX_PREFIX}/nginx.conf \
    && \
    cd /tmp/nginx-${NGINX_VERSION} && make && make install

###############################
FROM alpine:3.9
MAINTAINER ddl <itlab.ee.ncku.edu.tw>
ARG NGINX_PREFIX
ARG TZ

COPY --from=build-nginx ${NGINX_PREFIX} ${NGINX_PREFIX}

# Install packages
RUN apk add --update --no-cache \
    ca-certificates \
    openssl \
    pcre

RUN apk add --update --no-cache \
    nano logrotate

# Setup timezone
RUN apk add --update --no-cache tzdata && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    date && \
    apk del tzdata

# Cleanup
RUN rm -rf /var/cache/* /tmp/*

# Setup PATH
ENV PATH "${NGINX_PREFIX}/sbin:${PATH}"