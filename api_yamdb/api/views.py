from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import ThisAuthorOrReadOnly
from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
)
from reviews.models import Review, Title


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
