# FROM        python:3.7.3-alpine3.9
FROM        python:3-alpine3.9
MAINTAINER  ddl <itlab.ee.ncku.edu.tw>

RUN         mkdir /app
COPY        ./app/ /app/
RUN         pip install -r /app/requirements.txt

RUN         rm -rf /var/cache/* /tmp/*