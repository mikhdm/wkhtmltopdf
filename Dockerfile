FROM ubuntu:vivid
MAINTAINER Mikhaylenko Dmitry <mikhaylenko.dmitry@gmail.com>

ENV BUILD build-essential
 
RUN apt-get -y update -q \
	&& apt-get install --no-install-recommends -yq $BUILD python3 python3-pip wkhtmltopdf xvfb xauth xfonts-base \ 
	&& apt-get remove -y $BUILD \
	&& apt-get autoremove -y \
	&& apt-get clean \
	&& mkdir /root/wkhtmltopdf/

ADD wkhtmltopdf /root/wkhtmltopdf/

WORKDIR /root/wkhtmltopdf/
