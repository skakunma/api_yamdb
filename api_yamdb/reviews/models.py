from django.db import models

from .constants import LENGTH_LIMIT, MAX_LENGTH
from users.models import User


class Category(models.Model):
    name = models.CharField('Название', max_length=MAX_LENGTH)
    slug = models.SlugField('slug', max_length=50, unique=True)

    class Meta:

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:LENGTH_LIMIT]


class Genre(models.Model):
    name = models.CharField('Название', max_length=MAX_LENGTH)
    slug = models.SlugField('slug', max_length=50, unique=True)

    class Meta:

        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:LENGTH_LIMIT]


class Title(models.Model):
    name = models.CharField('Название', max_length=MAX_LENGTH)
    year = models.IntegerField('Год',)
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    class Meta:

        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LENGTH_LIMIT]


class Review(models.Model):
    """
    Класс Review.

    Класс Review описывает модель отзыва на
    произведение.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    text = models.TextField('Текст')
    score = models.PositiveSmallIntegerField('Оценка')
    pub_date = models.DateTimeField(
        'Дата добавления отзыва', auto_now_add=True, db_index=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:LENGTH_LIMIT]


class Comment(models.Model):
    """
    Класс Comment.

    Класс Comment описывает модель комментария к
    отзывам пользователей.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления комментария', auto_now_add=True, db_index=True)

    class Meta:

        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('pub_date',)
