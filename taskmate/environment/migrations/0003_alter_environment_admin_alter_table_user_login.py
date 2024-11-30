# Generated by Django 5.0.9 on 2024-11-30 16:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('environment', '0002_alter_environment_table_alter_table_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_environments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='table',
            name='user_login',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tables', to=settings.AUTH_USER_MODEL),
        ),
    ]
