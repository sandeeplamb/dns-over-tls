# DNS-Over-TLS

Sunday-Fun 
By Star-Lord
From-KnowWhere.

## The Goal

To send DNS resolution requests over TLS. More details here [dns-over-tls](https://developers.cloudflare.com/1.1.1.1/dns-over-tls/).

## Difficulty Level

`Saving Galaxy was much Easier.`

## Architecture

## Pre-requisites

* **[docker](https://www.docker.com/)** to create containers.

* **[python](https://www.python.org/)** to create server and client to listen requests.

* **[stubby](https://dnsprivacy.org/wiki/display/DP/About+Stubby)** proxy to handle tls.

* **[supervisor](http://supervisord.org/)** to run multiple processes.

* **[dig](https://linux.die.net/man/1/dig)** to run domain commands.

## Steps

1. Write Python Server and Client Socket programs to handle domain requests.

2. Update stubby YAML file to handle dns over tls.

3. Write Dockerfile.

4. Create Image and run container.

5. Run the tests.

### Step-01-Write-Python

The [server](https://github.com/sandeeplamb/dns-over-tls/blob/master/configs/server_dns.py)  and [client](https://github.com/sandeeplamb/dns-over-tls/blob/master/configs/client_dns.py) are written in python.

Server will be running as daemon in the container and will serve all the requests to client using the localhost DNS server run by Stubby.

Client needs Domain name as one arguement to run. The command will be `client_dns.py DNS_NAME`.

Server will run the command `dig @localhost DNS_NAME` and sent back the results to client.

### Step-02-Update-Stubby-Yaml

Stubby will be the doing the real magic to call the CloudFlare DNS-Over-TLS server over 853 port.

Inside [stubby.yaml](https://github.com/sandeeplamb/dns-over-tls/blob/master/configs/stubby.yml), we can use many *upstream_recursive_servers* in same config, but we need just one.

upstream_recursive_servers config looks like

```
upstream_recursive_servers:
  - address_data: 1.1.1.1
    tls_port: 853
    tls_auth_name: "cloudflare-dns.com"
```

### Step-03-Write-Dockerfile

Writing [Dockerfile](https://github.com/sandeeplamb/dns-over-tls/blob/master/configs/Dockerfile) is the easiest part.

We included all the necessary softwares inside the Dockerfile which will be helpful to make container run happily.

### Step-04-Create-Image-Container

Below are the steps to create the docker image.

```
[slamba ◯  Star-Lord ] ☘ mkdir dotls && cd dotls
[slamba ◯  Star-Lord ] ☘ git clone https://github.com/sandeeplamb/dns-over-tls.git .
[slamba ◯  Star-Lord ] ☘ cd configs
[slamba ◯  Star-Lord ] ☘ docker stop dotls
[slamba ◯  Star-Lord ] ☘ docker rm dotls
[slamba ◯  Star-Lord ] ☘ docker rmi dotls 
[slamba ◯  Star-Lord ] ☘ docker build -t dotls .
[slamba ◯  Star-Lord ] ☘ docker images dotls
```

We now need to run the container using above image.

Below commands will be helpful to run it.

```
[slamba ◯  Star-Lord ] ☘ docker run --name dotls -d --restart=always -p 53:53/udp dotls
[slamba ◯  Star-Lord ] ☘ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                NAMES
16dbd4b64201        dotls               "/usr/bin/supervisord"   37 minutes ago      Up 37 minutes       0.0.0.0:53->53/udp   dotls
```

### Step-05-Run-and-Test

Last step will be to see if all is ok.

Here are commands to check. We can make alias to this command as well.

`alias letsdig='docker exec dotls /opt/client_dns.py '`

```
[slamba ◯  Star-Lord ] ☘ letsdig duckduckgo.org
Sending the command...

; <<>> DiG 9.11.3-1ubuntu1.3-Ubuntu <<>> @localhost duckduckgo.org
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 45668
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1452
; PAD: 00 00 00 00 00 ("..................................................................................")
;; QUESTION SECTION:
;duckduckgo.org.			IN	A

;; ANSWER SECTION:
duckduckgo.org.		60	IN	A	107.20.240.232
duckduckgo.org.		60	IN	A	184.72.104.138
duckduckgo.org.		60	IN	A	23.21.193.169

;; Query time: 184 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Sun Jan 20 17:56:29 UTC 2019
;; MSG SIZE  rcvd: 510
```

**See it, To Believe it**

<p align="center">
  <a href="https://asciinema.org/a/o3l2QUySnxR3C2AvmTJKVM8x1?speed=3&amp;autoplay=1">
  <img src="https://asciinema.org/a/o3l2QUySnxR3C2AvmTJKVM8x1.png" width="885"></image>
  </a>
</p>

## Bonus-From-Star-Lord

There is a log file inside the container which records all the requests sent from client.

You can see the logs like

```
[slamba ◯  Star-Lord ] ☘ docker exec dotls cat /server_dns.py-history.log
Sun, 20 Jan 2019 17:52:01 INFO Checking domain duckduckgo.org
Sun, 20 Jan 2019 17:52:01 INFO Running command dig @localhost duckduckgo.org
Sun, 20 Jan 2019 17:56:29 INFO Checking domain duckduckgo.org
Sun, 20 Jan 2019 17:56:29 INFO Running command dig @localhost duckduckgo.org
Sun, 20 Jan 2019 18:31:13 INFO Checking domain google.com
Sun, 20 Jan 2019 18:31:13 INFO Running command dig @localhost google.com
```

**1. What are the security concerns for this kind of service?**

**2. In a microservice arch; how would you see this the dns to dns-over-tls proxy used?**

**3. What other improvements would be interesting to add to the project?**