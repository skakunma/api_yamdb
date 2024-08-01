from rest_framework import serializers
from .models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")


class UserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('id', 'confirmation_code', 'password')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "role", "first_name",
                  "last_name", "bio")
