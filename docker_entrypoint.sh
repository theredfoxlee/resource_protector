#!/usr/bin/env sh

export DJANGO_CUSTOM_SECRETKEY="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 60 | head -n 1)"

if [ -z "${DJANGO_CUSTOM_DEBUG}" ]; then
    export DJANGO_CUSTOM_DEBUG='0'
fi

if [ -z "${DJANGO_CUSTOM_ALLOWED_HOSTS}" ]; then
    export DJANGO_CUSTOM_ALLOWED_HOSTS='*'
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

if [ -z "${POSTGRES_DB_NAME}" ]; then
    export POSTGRES_DB_NAME='rpdatabase'
fi

if [ -z "${POSTGRES_DB_USER}" ]; then
    export POSTGRES_DB_USER='admin'
fi

if [ -z "${POSTGRES_DB_PASSWORD}" ]; then
    export POSTGRES_DB_PASSWORD='admin'
fi

if [ -z "${POSTGRES_DB_HOST}" ]; then
    export POSTGRES_DB_HOST='db'
fi

if [ -z "${POSTGRES_DB_PORT}" ]; then
    export POSTGRES_DB_PORT='5432'
fi

# -- Mandatory.

if [ -z "${POSTGRES_DB_HOST}" ]; then
    echo '** ERROR: env not set: POSTGRES_DB_HOST' 1>&2
    exit 1
fi


if [ -z "${AWS_S3_ENDPOINT_URL}" ]; then
    echo '** ERROR: env not set: AWS_S3_ENDPOINT_URL' 1>&2
    exit 1
fi

if [ -n "${ENTRYPOINT_DELAY_S}" ]; then
    sleep "${ENTRYPOINT_DELAY_S}"
fi

python manage.py migrate
python manage.py createsuperuser --noinput
echo yes | python manage.py collectstatic

echo -ne "[default]\naccess_key = ${AWS_SECRET_ACCESS_KEY}\nsecret_key = ${AWS_SECRETKEY_ID}\nhost_base = "${AWS_S3_ENDPOINT_URL}"\nhost_bucket = "${AWS_S3_ENDPOINT_URL}"\nhuman_readable_sizes = True\nmultipart_chunk_size_mb = 512\n" > ./s3cfg

s3cmd -c ./s3cfg --no-ssl mb "s3://${AWS_STORAGE_BUCKET_NAME}"

exec "$@"
