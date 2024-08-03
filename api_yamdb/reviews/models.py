from django.contrib.auth import get_user_model
from django.db import models

from django.db import models

User = get_user_model()


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
