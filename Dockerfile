FROM python:3.9.8-slim-bullseye
RUN mkdir /xd
WORKDIR /xd
COPY . .
RUN apt update; apt install -yy apache2; pip3 install -r requirements.txt
CMD ["bash","run.sh"]

run.sh

#!/bin/bash
# PORT 10000 for render.com webapp
sed -i "s/Listen 80/Listen 10000/" /etc/apache2/ports.conf
/etc/init.d/apache2 start
python3 main.py
