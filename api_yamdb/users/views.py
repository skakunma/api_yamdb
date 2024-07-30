from rest_framework import generics, status
from .models import User
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny


class SignUp(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid() and serializer.validated_data.get('username') != 'me':
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data) 
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
