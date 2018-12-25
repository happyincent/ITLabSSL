FROM python:3.7.1-alpine3.8
MAINTAINER ddl <itlab.ee.ncku.edu.tw>

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add --no-cache \
        nano \
        gcc musl-dev

RUN mkdir -p mkdir /www
WORKDIR /www

COPY ./app/requirements.txt /www/requirements.txt
RUN pip install -r requirements.txt

RUN sed -i "s|return uri|return 'https://ssl.itlab.ee.ncku.edu.tw:62400/' + uri.partition('//')[2].partition('/')[2]|" /usr/local/lib/python3*/site-packages/allauth/utils.py

# Setting the timezone
RUN apk add tzdata && \
  cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime && \
  echo "Asia/Taipei" >  /etc/timezone && \
  date && \
  apk del tzdata