
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [

        ('environment', '0004_remove_table_user_login'),

        ('task', '0003_alter_task_assigned_to_alter_task_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='table',

            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='environment.table'),

        ),
    ]
