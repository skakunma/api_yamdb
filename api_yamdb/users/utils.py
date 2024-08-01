import random
import string
from django.core.mail import send_mail

def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits,
                                  k=length))

def send_verification_email(email, code):
    subject = 'Your Verification Code'
    message = f'Your verification code is {code}'
    from_email = 'skakunda@mail.ru'
    send_mail(subject, message, from_email, [email])
