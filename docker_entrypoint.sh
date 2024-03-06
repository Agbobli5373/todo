# #!/bin/sh
# cd /app
# source .venv/bin/activate


# if [[ "$1" == "celery-worker" ]]; then
#     celery -A todomir worker  -l INFO
# elif [[ "$1" == "celery-beat" ]]; then
#     celery -A todomir worker --beat -l INFO
# else
#     python manage.py collectstatic --noinput
#     python manage.py migrate 
#     python manage.py nginx
#     gunicorn --config $GUNICORN_CONFIG
# fi
