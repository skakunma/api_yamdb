from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,)

from .mixins import ListCreateDestroyMixin
from .permissions import ThisAuthorOrReadOnly, AdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleReadOnlySerializer)
from reviews.models import Category, Genre, Review, Title



class CategoryViewSet(ListCreateDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = [AdminOrReadOnly,]


class GenreViewSet(ListCreateDestroyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = [AdminOrReadOnly,]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year',)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [AdminOrReadOnly,]


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreateSerializer
        return TitleReadOnlySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Класс ReviewViewSet.
    Класс ReviewViewSet описывает API-представление отзывов.
    Предоставляет следующие запросы: GET, POST,
    PATCH, DELETE.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ThisAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        """
        Метод get_title.
        Метод get_title возвращает объект
        отдельного произведения.
        """
        return get_object_or_404(
            Title,
            id=self.kwargs.get("title_id")
        )

    def get_queryset(self):
        """
        Метод get_queryset.
        Метод get_queryset описывает получение набора
        объектов/одного объекта модели.
        """
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """
        Метод perform_create.
        Метод perform_create описывает создание новых
        объектов модели.
        """
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    Класс CommentViewSet.
    Класс CommentViewSet описывает API-представление комментариев.
    Предоставляет следующие запросы: GET, POST,
    PATCH, DELETE.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ThisAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        """
        Метод get_title.
        Метод get_title возвращает объект
        отдельного произведения.
        """
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id")
        )

    def get_queryset(self):
        """
        Метод get_queryset.
        Метод get_queryset описывает получение набора
        объектов/одного объекта модели.
        """
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """
        Метод perform_create.
        Метод perform_create описывает создание новых
        объектов модели.
        """
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
