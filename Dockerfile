FROM ubuntu:latest

RUN mkdir sampleEx
WORKDIR /sampleEx
COPY /cve-2013-2028 /sampleEx

RUN apt update && \
	apt install git -y && \
	apt install gcc -y && \
	apt install make

Run apt install python2.7 -y && \  
	apt install python-pip -y
RUN pip install pwntools

RUN ./setup.sh

WORKDIR /sampleEx/nginx/conf
RUN mv fastcgi.conf fastcgi_params koi-utf koi-win mime.types scgi_params uwsgi_params win-utf /sampleEx/run/conf
WORKDIR /sampleEx
