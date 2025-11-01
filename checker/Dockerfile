FROM python:3.13.3-alpine3.22

ARG USER="app"
ARG GROUP="app"

ENV PATH="/home/${USER}/.local/bin:${PATH}"
ENV TZ="UTC"
ENV PYTHONUNBUFFERED=1

RUN addgroup -S ${GROUP} \
    && adduser -S ${USER} -G ${GROUP}

USER ${USER}
WORKDIR /home/${USER}

COPY --chown=${USER} app.py ssl_checks.py requirements.txt hosts.lst /home/${USER}/

RUN pip install -r requirements.txt

CMD python -u app.py
