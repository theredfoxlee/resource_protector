#!/usr/bin/env sh

python manage.py migrate
python manage.py createsuperuser --noinput

exec "$@"
