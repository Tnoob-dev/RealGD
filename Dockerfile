FROM python:3.9.8-slim-bullseye
RUN mkdir /xd
WORKDIR /xd
COPY . .
RUN apt update; apt install -yy apache2; pip3 install -r requirements.txt
CMD ["bash","run.sh"]
