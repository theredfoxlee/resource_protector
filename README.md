# resource_protector

A blob storage.

## usage

resource_protector is running on port **8000**.

```bash
docker build . -t theredfoxlee/resource_protector:latest
docker run --env-file custom_envs -p 80:8000 theredfoxlee/resource_protector:latest
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
