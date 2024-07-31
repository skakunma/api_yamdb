from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)
from reviews.models import Category, Comment, Genre, Review, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year',)
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Класс ReviewViewSet.
    Класс ReviewViewSet описывает API-представление отзывов.
    Предоставляет следующие запросы: GET, POST,
    PUT, PATCH, DELETE.
    """

    serializer_class = ReviewSerializer
    #permission_classes = [AuthorPermission]
    pagination_class = LimitOffsetPagination

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
    PUT, PATCH, DELETE.
    """

    serializer_class = CommentSerializer
    #permission_classes = (permissions.AllowAny,)
    pagination_class = LimitOffsetPagination

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
