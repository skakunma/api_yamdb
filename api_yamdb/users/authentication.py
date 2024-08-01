import jwt

from django.conf import settings
from .models import User

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class JSONWebTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            # Декодирование JWT токена
            payload = jwt.decode(key, 'p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs', algorithms=['HS256'])
            user = User.objects.get(username=payload['username'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        return (user, payload)
