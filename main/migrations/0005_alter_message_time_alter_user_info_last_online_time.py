# Generated by Django 4.2.2 on 2023-07-14 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_group_description_alter_message_attached_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.DateField(default=datetime.datetime(2023, 7, 14, 20, 18, 29, 632844, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='user_info',
            name='last_online_time',
            field=models.DateField(default=datetime.datetime(2023, 7, 14, 20, 18, 29, 633080, tzinfo=datetime.timezone.utc)),
        ),
    ]
