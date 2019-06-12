# FROM python:3.7.3-alpine3.9
FROM python:3-alpine3.9
MAINTAINER ddl <itlab.ee.ncku.edu.tw>

# Environment
ENV PYTHONUNBUFFERED 1
ARG TZ=Asia/Taipei

RUN mkdir -p mkdir /www
WORKDIR /www

# pip install
COPY ./app/requirements.txt /www/requirements.txt
RUN apk add --update --no-cache openssl-dev
RUN set -e; \
    apk update \
    && apk add --virtual .build-deps gcc build-base python3-dev linux-headers musl-dev libffi-dev \
    && pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r /www/requirements.txt \
    && apk del .build-deps

# Setup django-allauth==0.39.1 's email uri
RUN sed -i "s|return uri|return 'https://ssl.itlab.ee.ncku.edu.tw/' + uri.partition('//')[2].partition('/')[2]|" /usr/local/lib/python3*/site-packages/allauth/utils.py

# Install packages
RUN apk add --update --no-cache nano logrotate
RUN apk add --update --no-cache supervisor

# Setup timezone
RUN apk add --update --no-cache tzdata && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    date && \
    apk del tzdata

# Cleanup
RUN rm -rf /var/cache/* /tmp/*