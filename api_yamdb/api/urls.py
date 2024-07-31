from django.urls import path
from users.views import SignUp, SignIn


urlpatterns = [
    path('auth/signup/', SignUp.as_view()),
    path('auth/token/', SignIn.as_view()),
]
