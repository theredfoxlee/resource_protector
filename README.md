# keeper

A blob storage.

## usage

keeper is running on port **8000**.

```bash
docker build . -t theredfoxlee/keeper:latest
docker run --env-file custom_envs -p 80:8000 theredfoxlee/keeper:latest
```

### custom_envs

The following envs have to be placed in `./custom_envs` file.

```bash
DJANGO_CUSTOM_SECRETKEY=<SECRET_KEY_STR>
DJANGO_CUSTOM_DEBUG=<ANYTHING>

DJANGO_SUPERUSER_USERNAME=<USERNAME>
DJANGO_SUPERUSER_PASSWORD=<PASSWORD>
DJANGO_SUPERUSER_EMAIL=<EMAIL>
```
