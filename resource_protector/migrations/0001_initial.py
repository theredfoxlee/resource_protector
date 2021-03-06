# Generated by Django 3.2.4 on 2021-06-23 00:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import resource_protector.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_agent', models.CharField(default=None, max_length=1000, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProtectedUrlModel',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('password', models.CharField(default=None, max_length=150, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('accesses', models.IntegerField(default=0)),
                ('url', models.URLField(max_length=2048)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProtectedFileModel',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('password', models.CharField(default=None, max_length=150, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('accesses', models.IntegerField(default=0)),
                ('file', models.FileField(upload_to=resource_protector.models._upload_to)),
                ('original_name', models.CharField(max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
