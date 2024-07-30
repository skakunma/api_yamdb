from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class User(models.Model):
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Введите корректный адрес электронной почты.")]
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\w+$',
                message='Username must match the regex ^w\\Z'
            )
        ]
    )

    def __str__(self):
        return self.username
