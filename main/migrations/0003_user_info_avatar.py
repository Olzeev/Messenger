# Generated by Django 4.2.2 on 2023-07-12 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_group_avatar_remove_user_info_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='avatar',
            field=models.ImageField(default='static/main/png/default_avatar.jpg', upload_to='user_avtrs'),
        ),
    ]