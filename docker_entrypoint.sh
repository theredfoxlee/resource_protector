#!/usr/bin/env sh

export DJANGO_CUSTOM_SECRETKEY="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 60 | head -n 1)"

if [ -z "${DJANGO_CUSTOM_DEBUG}" ]; then
    export DJANGO_CUSTOM_DEBUG='0'
fi

if [ -z "${DJANGO_SUPERUSER_USERNAME}" ]; then
    export DJANGO_SUPERUSER_USERNAME='admin'
fi

if [ -z "${DJANGO_SUPERUSER_PASSWORD}" ]; then
    export DJANGO_SUPERUSER_PASSWORD='admin'
fi

if [ -z "${DJANGO_SUPERUSER_EMAIL}" ]; then
    export DJANGO_SUPERUSER_EMAIL='admin@gmail.com'
fi

if [ -z "${AWS_ACCESS_KEY_ID}" ]; then
    export AWS_ACCESS_KEY_ID='dummy'
fi

if [ -z "${AWS_SECRET_ACCESS_KEY}" ]; then
    export AWS_SECRET_ACCESS_KEY='dummy'
fi

if [ -z "${AWS_STORAGE_BUCKET_NAME}" ]; then
    export AWS_STORAGE_BUCKET_NAME='rpstorage'
fi

# -- Mandatory.
if [ -z "${AWS_S3_ENDPOINT_URL}" ]; then
    echo '** ERROR: env not set: AWS_S3_ENDPOINT_URL' 1>&2
    exit 1
fi

python manage.py migrate
python manage.py createsuperuser --noinput

exec "$@"
