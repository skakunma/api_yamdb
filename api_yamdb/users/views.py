from rest_framework import generics, status
from .models import User
from rest_framework.response import Response
from .serializers import (UserSignUpSerializer, UserSignInSerializer,
                          UserListSerializer, UserCreateSerializer)
from .utils import generate_verification_code
from rest_framework.permissions import AllowAny
from .permissions import IsAdminUser
from django.shortcuts import get_object_or_404
import jwt
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
import datetime
from django.conf import settings
from rest_framework.filters import SearchFilter
import uuid


class SignUp(generics.CreateAPIView):
    model = User
    serializer_class = UserSignUpSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()
                and serializer.validated_data.get('username') != 'me'):
            verification_code = generate_verification_code()
            send_mail(
                'Your Verification Code',
                f'Your verification code is {verification_code}.',
                'api_yamdb@mail.ru',
                [serializer.validated_data.get('email')],
                fail_silently=False,
            )
            self.perform_create(serializer)
            user = User.objects.get(
                username=serializer.validated_data.get('username'))
            user.confirmation_code = verification_code
            user.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK,
                            headers=headers)

        if (User.objects.filter(email=request.data.get('email'))
                and User.objects.filter(
                    username=request.data.get('username'))):

            verification_code = generate_verification_code()
            send_mail(
                'Your Verification Code',
                f'Your verification code is {verification_code}.',
                settings.EMAIL,
                [request.data.get('email')],
                fail_silently=False,
            )
            user = User.objects.get(username=request.data.get('username'))
            user.confirmation_code = verification_code
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(generics.CreateAPIView):
    model = User
    serializer_class = UserSignInSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        if (request.data.get('username')
                and request.data.get('confirmation_code')):
            user = get_object_or_404(User,
                                     username=request.data.get('username'))

            if user.confirmation_code == request.data.get('confirmation_code'):
                jti = str(uuid.uuid4())
                payload = {
                    'username': user.username,
                    'token_type': 'access',
                    'jti': jti,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(
                        hours=1),
                    'iat': datetime.datetime.utcnow()  # Время создания токена
                }

                encoded_jwt = jwt.encode(payload, settings.SECRET_KEY,
                                         algorithm='HS256')

                return Response({
                    'token': encoded_jwt
                }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ListUsers(generics.ListAPIView):
    model = User
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdminUser, ]
    filter_backends = [SearchFilter]
    search_fields = ['username']

    def get_queryset(self):
        return User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser, ]
    lookup_field = 'username'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UsersMe(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data.pop('role', None)

        user = self.get_object()
        serializer = self.get_serializer(user, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
