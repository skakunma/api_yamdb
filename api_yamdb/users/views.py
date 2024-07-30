from rest_framework import generics, status
from .models import User
from rest_framework.response import Response
from .serializers import UserSerializer
from .utils import generate_verification_code, send_verification_email
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail


class SignUp(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() and serializer.validated_data.get('username') != 'me':
            verification_code = generate_verification_code()
            
            # Сохранение нового пользователя с кодом подтверждения
            serializer.save(verification_code=verification_code)
            
            # Отправка email с кодом подтверждения
            send_mail(
                'Your Verification Code',
                f'Your verification code is {verification_code}.',
                'no-reply@example.com',  # Замените на ваш email отправителя
                [serializer.validated_data.get('email')],
                fail_silently=False,
            )


            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

        if User.objects.filter(email=request.data.get('email')) and User.objects.filter(username=request.data.get('username')):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
