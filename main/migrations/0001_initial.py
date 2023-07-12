# Generated by Django 4.2.2 on 2023-06-27 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=30)),
                ('avatar', models.FileField(upload_to='')),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='Group_ref',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.CharField(max_length=10)),
                ('user_id', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Group reference',
                'verbose_name_plural': 'Group references',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_sender', models.CharField(max_length=10)),
                ('id_reciever', models.CharField(max_length=10)),
                ('text', models.TextField()),
                ('time', models.DateField()),
                ('attached_file', models.FileField(upload_to='')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='User_blocked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=10)),
                ('id_user_blocked', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'User blocked',
                'verbose_name_plural': 'Users blocked',
            },
        ),
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_info_id', models.CharField(max_length=10)),
                ('avatar', models.FileField(upload_to='')),
                ('status', models.TextField()),
                ('last_online_time', models.DateField()),
            ],
            options={
                'verbose_name': 'User info',
                'verbose_name_plural': "Users' info",
            },
        ),
    ]