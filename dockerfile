from ubuntu:18.04

RUN apt update
RUN apt install python3.8 python3-pip -y

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir /opt/app
RUN mkdir /opt/mail
WORKDIR /opt/app

COPY . .