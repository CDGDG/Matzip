FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y dist-upgrade
RUN apt-get install -y apt-utils dialog libpq-dev

RUN apt-get install -y python3-pip python3-dev

RUN apt-get install -y libssl-dev
RUN apt-get install -y mysql-server
RUN apt-get install -y mysql-client
RUN apt-get install -y libmysqlclient-dev

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

ADD requirements.txt /config/
RUN pip3 install -r /config/requirements.txt

WORKDIR /src
