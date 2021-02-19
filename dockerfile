from python:3.8

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir /opt/app
RUN mkdir /opt/mail
WORKDIR /opt/app

COPY . .