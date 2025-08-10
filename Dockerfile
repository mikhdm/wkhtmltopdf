FROM python:3.11-slim-bullseye

ENV BUILD=build-essential

# wkhtmltopdf dependency libjped-turbo 
ADD https://packagecloud.io/dcommander/libjpeg-turbo/gpgkey .
ADD https://raw.githubusercontent.com/libjpeg-turbo/repo/main/libjpeg-turbo.list .

RUN apt-get update -yq \
	&& apt-get install --no-install-recommends -yq $BUILD gpg xvfb xauth xfonts-base xfonts-75dpi libxrender1 fontconfig \ 
	&& apt-get remove -y $BUILD \
	&& apt-get autoremove -y \
	&& apt-get clean \
	&& mkdir /root/wkhtmltopdf

RUN cat gpgkey | gpg --dearmor >/etc/apt/trusted.gpg.d/libjpeg-turbo.gpg && \
    mv libjpeg-turbo.list /etc/apt/sources.list.d/ && apt-get -y update && apt-get install -yq libjpeg62-turbo && apt-get clean && rm -f gpgkey 

ADD https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb .

# installing wkhtmltopdf
RUN dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb && rm -f wkhtmltox_0.12.6-1.buster_amd64.deb

COPY wkhtmltopdf /root/wkhtmltopdf/
WORKDIR /root/wkhtmltopdf

EXPOSE 8000

ENTRYPOINT []
CMD ["/bin/sh", "-c", "./server.py", "0.0.0.0:8000"]
