from rest_framework import serializers
from .models import User
from django.shortcuts import get_object_or_404


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", )
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.generate_verification_code()  # Генерация и сохранение кода подтверждения
        user.send_verification_email()     # Отправка email с кодом
        return user
