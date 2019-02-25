# FROM python:3.7.2-alpine3.9
FROM python:3-alpine3.9
MAINTAINER ddl <itlab.ee.ncku.edu.tw>

# Environment
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Taipei

RUN mkdir -p mkdir /www
WORKDIR /www

# Installation
RUN apk update
RUN apk add --update --no-cache \
        nano logrotate \
        gcc musl-dev \
        libffi-dev openssl-dev

COPY ./app/requirements.txt /www/requirements.txt
RUN pip install -r requirements.txt

# Setup django-allauth's email uri
RUN sed -i "s|return uri|return 'https://ssl.itlab.ee.ncku.edu.tw:62400/' + uri.partition('//')[2].partition('/')[2]|" /usr/local/lib/python3*/site-packages/allauth/utils.py

# Setup timezone
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    date && \
    apk del tzdata

# Setup scripts
COPY crontab /crontab
COPY run.sh /run.sh
RUN chmod 775 /run.sh
RUN find /etc/periodic/ -type f -exec rm {} \;

# Setup supervisord
RUN apk add --no-cache supervisor
COPY supervisord.conf /etc/supervisord.conf

# Cleanup
RUN rm -rf /var/cache/* /tmp/*