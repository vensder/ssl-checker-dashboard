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

COPY --chown=${USER} app.py slack_post.py requirements.txt /home/${USER}/

RUN pip install -r requirements.txt

CMD python -u app.py
