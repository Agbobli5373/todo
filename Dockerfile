FROM python:3.12-alpine
MAINTAINER jkawczynski

ENV APP_ROOT=/app
ENV SRV_ROOT=/srv
ENV GUNICORN_CONFIG=/srv/gunicorn/config.py
ENV VENV_PATH=/opt/venv
ENV PROD=true

RUN apk update && apk add nginx \
  apk add openrc \
  rm -rf /var/cache/apk/*

RUN adduser --uid 1000 app --gecos app --disabled-password

RUN touch /var/run/nginx.pid && \
    mkdir /var/cache/nginx && \
    chown -R app:app /var/run/nginx.pid && \
    chown -R app:app /var/log/nginx && \
    chown -R app:app /var/lib/nginx && \
    chown -R app:app /var/cache/nginx

RUN pip install uv

ADD requirements.txt $APP_ROOT/
WORKDIR $APP_ROOT
RUN uv venv
RUN uv pip install gunicorn && \
    uv pip install -r requirements.txt

ADD etc/nginx/nginx.conf /etc/nginx/nginx.conf
ADD etc/gunicorn/* $SRV_ROOT/gunicorn/
ADD todomir $APP_ROOT/
ADD docker_entrypoint.sh $SRV_ROOT

RUN mkdir $SRV_ROOT/db/ && touch $SRV_ROOT/db/db.sqlite3

RUN chmod +x $SRV_ROOT/docker_entrypoint.sh && \
    chown app:app -R $APP_ROOT && \
    chown app:app -R $SRV_ROOT

USER app

EXPOSE 8000
ENTRYPOINT ["/srv/docker_entrypoint.sh"]
