import random
import string
from django.core.mail import send_mail


def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits,
                                  k=length))
