# SSL Checker Dashboard

[![Python application](https://github.com/vensder/ssl-checker-dashboard/workflows/Python%20application/badge.svg)](https://github.com/vensder/ssl-checker-dashboard/actions?query=workflow%3A%22Python+application%22)

SSL Checker Dashboard builded using Bottle Python micro web-framework (Work In Progress).

The dashboard allows you to overview the expiration days for the SSL certificates of the domains from the `cron/domains.lst` file.

![SSL Checker Dashboard](./img/screenshot.png?raw=true)

## How to run locally

```bash
docker-compose build
docker-compose up -d cron redis
sleep 10
docker-compose up -d web-app
docker-compose ps
```

Open the link in a browser: <http://localhost:8080/>

## Run load test

```bash
ab -c 100 -n 10000 http://127.0.0.1:8080/all
```
