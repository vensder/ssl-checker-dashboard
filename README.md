# SSL Checker Dashboard

SSL Checker Dashboard builded using Bottle Python micro web-framework (Work In Progress).

The dashboard allows you to overview the expiration days for the SSL certificates of the domains from the 'domains.lst' file.

![SSL Checker Dashboard](./img/screenshot.png?raw=true)

## How to run locally

```bash
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
cd microservices/scheduler && docker-compose up -d
cd -
./app.py
```

## Run with gunicorn

```bash
gunicorn -b 0.0.0.0:8080 app:app
```
