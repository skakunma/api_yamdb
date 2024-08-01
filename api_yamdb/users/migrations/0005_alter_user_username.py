# Generated by Django 3.2.25 on 2024-08-01 10:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Username должен быть формата^[w.@+-]+Z', regex='^[\\w.@+-]+$')]),
        ),
    ]
