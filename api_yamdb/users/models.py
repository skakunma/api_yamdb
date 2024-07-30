from django.db import models
from django.core.validators import EmailValidator, RegexValidator
import random
import string

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
    verification_code = models.CharField(
        max_length=6,
        blank=True,
        null=True)
    
    def __str__(self):
        return self.username
    
    def generate_verification_code(self):
        """Генерация случайного кода подтверждения"""
        self.verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        self.save()

    def send_verification_email(self):
        """Отправка email с кодом подтверждения"""
        from django.core.mail import send_mail
        send_mail(
            'Your Verification Code',
            f'Your verification code is {self.verification_code}.',
            'from@example.com',
            [self.email],
            fail_silently=False,
        )
