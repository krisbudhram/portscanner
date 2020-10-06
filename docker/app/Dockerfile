FROM python:3.8

# Install Nmap
RUN apt-get update && apt-get install -y  nmap && rm -rf /var/lib/apt/lists/*

ADD . /opt/portscanner

WORKDIR /opt/portscanner

