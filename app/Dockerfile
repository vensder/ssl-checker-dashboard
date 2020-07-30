FROM python:3.8.5-alpine3.12

ARG USER="app"
ARG GROUP="app"

ENV PATH="/home/${USER}/.local/bin:${PATH}"
ENV TZ="UTC"
ENV PYTHONUNBUFFERED=1

RUN addgroup -S ${GROUP} \
    && adduser -S ${USER} -G ${GROUP}

USER ${USER}
WORKDIR /home/${USER}

COPY --chown=${USER} . /home/${USER}/

RUN pip install -r requirements.txt --user

ENTRYPOINT [ "gunicorn", "app:app" ]

CMD ["--worker-tmp-dir /dev/shm", "--log-file=-", "-b 0.0.0.0:8080", "-w 1"]
