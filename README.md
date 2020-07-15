# SSL Checker Dashboard

SSL Checker Dashboard builded using Bottle Python micro web-framework (Work In Progress).

The dashboard allows you to overview the expiration days for the SSL certificates of the domains from the 'domains.lst' file.

![SSL Checker Dashboard](./img/screenshot.png?raw=true)

## How to run locally

```bash
virtualenv -p python env
source env/bin/activate
pip install -r requirements.txt
./app.py
```

## How to run with Redis

```bash
docker run --rm --name my-redis -p 6379:6379 -d redis:6.0.5-alpine
virtualenv -p python env
source env/bin/activate
pip install -r requirements.txt
./app.py
```

## Run with gunicorn

```bash
gunicorn -b 0.0.0.0:8080 app:app
```
