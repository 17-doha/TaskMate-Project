# Generated by Django 5.0.9 on 2024-11-28 14:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('environment_id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
                ('is_private', models.BooleanField(default=False)),
                ('admin_login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_environments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('table_id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
                ('environment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='environment.environment')),
                ('user_login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tables', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
