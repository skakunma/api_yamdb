# Generated by Django 3.2 on 2024-07-31 07:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin')], default='user', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Username must match the regex ^[\\w.@+-]+\\Z', regex='^[\\w.@+-]+$')]),
        ),
    ]
