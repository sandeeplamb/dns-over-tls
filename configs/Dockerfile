FROM ubuntu:latest
LABEL MAINTAINER "Sandeep Lamba"

RUN \
  apt-get update \
  && apt-get install -y software-properties-common \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils vim wget tcpdump stubby \ 
     net-tools python3-pip supervisor \
  && pip3 install dnspython \
  && rm -rf /var/lib/apt/lists/*

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY stubby.yml /etc/stubby/stubby.yml
COPY client_dns.py /opt
COPY server_dns.py /opt

RUN chmod 755 /opt/client_dns.py \ 
  && chmod 755 /opt/server_dns.py

EXPOSE 53:53/udp

ENTRYPOINT ["/usr/bin/supervisord"]