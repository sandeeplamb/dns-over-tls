# DNS-Over-TLS

## Create the Docker Image

```
[slamba ◯  Star-Lord ] ☘ docker stop dotls
[slamba ◯  Star-Lord ] ☘ docker rm dotls
[slamba ◯  Star-Lord ] ☘ docker rmi dotls 
[slamba ◯  Star-Lord ] ☘ docker build -t dotls .
[slamba ◯  Star-Lord ] ☘ docker images dotls
```

## Start the Container

```
[slamba ◯  Star-Lord ] ☘ docker run --name dotls -d --restart=always -p 53:53/udp dotls
[slamba ◯  Star-Lord ] ☘ docker ps
```

## Test the domain resolution

```
[slamba ◯  Star-Lord ] ☘ docker exec dotls /opt/client_dns.py duckduckgo.org
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