from django.urls import path
from users.views import SignUp


urlpatterns = [
    path('auth/signup/', SignUp.as_view()),
]
