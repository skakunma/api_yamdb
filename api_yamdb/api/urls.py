from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet)
from users.views import SignUp, SignIn, ListUsers, DetaliUsers

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignUp.as_view()),
    path('auth/token/', SignIn.as_view()),
    path('users/', ListUsers.as_view()),
    path('users/<str:username>/', DetaliUsers.as_view())
]
