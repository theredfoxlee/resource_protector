FROM python:3.9.5-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN \
 python3 -m pip install s3cmd --no-cache-dir

COPY . .

EXPOSE 8000

ENTRYPOINT ["./docker_entrypoint.sh"] 
CMD [\
    "gunicorn",\
    "resource_protector_project.wsgi:application",\
    "--bind", "0.0.0.0:8000",\
    "--access-logfile", "-"\
]

