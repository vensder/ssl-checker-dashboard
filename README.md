# SSL Checker Dashboard

[![Python application](https://github.com/vensder/ssl-checker-dashboard/workflows/Python%20application/badge.svg)](https://github.com/vensder/ssl-checker-dashboard/actions?query=workflow%3A%22Python+application%22)

The SSL Checker Dashboard allows you to overview the expiration days for the SSL certificates of the domains from the `cron/domains.lst` file.

The dashboard built using Bottle Python micro web-framework and Docker (Work In Progress). You can run it in Kubernetes (see `./k8s` directory)

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

## How to run in Kubernetes

Tested in MicroK8s: <https://microk8s.io/>

```bash
sudo microk8s enable ingress
```

```bash
kubectl apply -f ./k8s/web-app.yml
deployment.apps/web-app created
service/web-app created
ingress.networking.k8s.io/web-app created
service/redis created
deployment.apps/redis created
deployment.apps/cron created
```

```bash
kubectl get ingress
NAME      CLASS    HOSTS              ADDRESS     PORTS   AGE
web-app   <none>   ssl-checks.local   127.0.0.1   80      47s
```

Add `ssl-checks.local` host to `/etc/hosts` file:

```bash
grep ssl-checks /etc/hosts
127.0.0.1 ssl-checks.local
```

Open in browser: <http://ssl-checks.local/>

## How to copy your own domains list

You can copy your own domains list inside the `cron` container, and `cron` service will update the domains info for the new domains.

If you use docker-compose, just run the `cp` command:

```bash
docker cp your_domains.lst ssl-checker-dashboard_cron_1:/home/app/domains.lst
```

Or, if you use Kubernetes, copy your file inside the `cron` Pod, for example:

```bash
kubectl cp your_domains.lst default/cron-68c997f7c-c49hl:/home/app/domains.lst
```
