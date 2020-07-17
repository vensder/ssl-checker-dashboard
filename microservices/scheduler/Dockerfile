FROM python:3.8.4-alpine3.12

RUN addgroup -S app && adduser -S app -G app

WORKDIR /app

USER app

COPY app.py ssl_checks.py requirements.txt domains.lst /app/

RUN pip install -r requirements.txt

CMD python -u app.py
