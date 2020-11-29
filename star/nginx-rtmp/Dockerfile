# Mod: https://github.com/alfg/docker-nginx-rtmp/blob/master/Dockerfile

ARG NGINX_VERSION=1.16.0
ARG NGINX_RTMP_VERSION=1.2.1
ARG FFMPEG_VERSION=4.1.3

ARG NGINX_PREFIX=/opt/nginx
ARG FFMPEG_PREFIX=/usr/local
ARG MAKEFLAGS="-j16"
ARG TZ=Asia/Taipei

###############################
FROM alpine:3.9 as build-nginx
ARG NGINX_VERSION
ARG NGINX_RTMP_VERSION
ARG NGINX_PREFIX
ARG MAKEFLAGS

# Get nginx source
RUN cd /tmp && \
    wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && \
    tar zxf nginx-${NGINX_VERSION}.tar.gz && \
    rm nginx-${NGINX_VERSION}.tar.gz

# Get nginx-rtmp module
RUN cd /tmp && \
    wget https://github.com/arut/nginx-rtmp-module/archive/v${NGINX_RTMP_VERSION}.tar.gz && \
    tar zxf v${NGINX_RTMP_VERSION}.tar.gz && rm v${NGINX_RTMP_VERSION}.tar.gz && \
    sed -i 's/            case ESCAPE/            \/\/ fall through\n            case ESCAPE/' nginx-rtmp-module-${NGINX_RTMP_VERSION}/ngx_rtmp_eval.c

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
  --with-threads \
  --with-file-aio \
  --with-debug \
  --add-module=/tmp/nginx-rtmp-module-${NGINX_RTMP_VERSION} \
  --conf-path=${NGINX_PREFIX}/nginx.conf \
  && \
  cd /tmp/nginx-${NGINX_VERSION} && make && make install

###############################
FROM alpine:3.9 as build-ffmpeg
ARG FFMPEG_VERSION
ARG FFMPEG_PREFIX
ARG MAKEFLAGS

# Get FFmpeg source.
RUN cd /tmp/ && \
    wget http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz && \
    tar zxf ffmpeg-${FFMPEG_VERSION}.tar.gz && rm ffmpeg-${FFMPEG_VERSION}.tar.gz

# FFmpeg build dependencies
RUN apk add --update \
    build-base \
    coreutils \
    freetype-dev \
    lame-dev \
    libogg-dev \
    libass \
    libass-dev \
    libvpx-dev \
    libvorbis-dev \
    libwebp-dev \
    libtheora-dev \
    opus-dev \
    pkgconf \
    pkgconfig \
    rtmpdump-dev \
    wget \
    x264-dev \
    x265-dev \
    yasm \
    openssl-dev

RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
RUN apk add --update fdk-aac-dev

# Compile ffmpeg
RUN cd /tmp/ffmpeg-${FFMPEG_VERSION} && \
    ./configure \
    --prefix=${FFMPEG_PREFIX} \
    --enable-version3 \
    --enable-gpl \
    --enable-nonfree \
    --enable-small \
    --enable-libmp3lame \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libvpx \
    --enable-libtheora \
    --enable-libvorbis \
    --enable-libopus \
    --enable-libfdk-aac \
    --enable-libass \
    --enable-libwebp \
    --enable-librtmp \
    --enable-postproc \
    --enable-avresample \
    --enable-libfreetype \
    --enable-openssl \
    --disable-debug \
    --disable-doc \
    --disable-ffplay \
    --extra-libs="-lpthread -lm" && \
    make && make install && make distclean

###############################
FROM alpine:3.9
ARG NGINX_PREFIX
ARG FFMPEG_PREFIX
ARG TZ
MAINTAINER ddl <itlab.ee.ncku.edu.tw>

COPY --from=build-nginx ${NGINX_PREFIX} ${NGINX_PREFIX}
COPY --from=build-ffmpeg ${FFMPEG_PREFIX} ${FFMPEG_PREFIX}
COPY --from=build-ffmpeg /usr/lib/libfdk-aac.so.2 /usr/lib/libfdk-aac.so.2

# Install packages
RUN apk add --update --no-cache \
    ca-certificates \
    openssl \
    pcre

RUN apk add --update --no-cache \
    lame \
    libogg \
    libass \
    libvpx \
    libvorbis \
    libwebp \
    libtheora \
    opus \
    rtmpdump \
    x264-dev \
    x265-dev

RUN apk add --update --no-cache nano logrotate

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