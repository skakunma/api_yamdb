from django.db import models

from users.models import User

LENGTH_LIMIT = 50


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('slug', max_length=50, unique=True)

    def __str__(self):
        return self.name[:LENGTH_LIMIT]


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('slug', max_length=50, unique=True)

    def __str__(self):
        return self.name[:LENGTH_LIMIT]


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
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

    def __str__(self):
        return self.name[:LENGTH_LIMIT]


class Review(models.Model):
    """
    Класс Review.

    Класс Review описывает модель отзыва на
    произведение.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('Текст')
    score = models.IntegerField('Оценка')
    pub_date = models.DateTimeField(
        'Дата добавления отзыва', auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:LENGTH_LIMIT]


class Comment(models.Model):
    """
    Класс Comment.

    Класс Comment описывает модель комментария к
    отзывам пользователей.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления комментария', auto_now_add=True, db_index=True)
