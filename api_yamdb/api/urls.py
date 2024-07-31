from django.urls import path
from users.views import SignUp, SignIn, ListUsers, DetaliUsers


urlpatterns = [
    path('auth/signup/', SignUp.as_view()),
    path('auth/token/', SignIn.as_view()),
    path('users/', ListUsers.as_view()),
    path('users/<str:username>/', DetaliUsers.as_view())
]
