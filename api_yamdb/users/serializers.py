from rest_framework import serializers
from .models import User
from django.shortcuts import get_object_or_404



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
