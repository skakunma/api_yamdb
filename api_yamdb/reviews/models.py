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
        User, on_delete=models.CASCADE, related_name='reviews')
    # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='reviews')
    title = models.IntegerField()
    text = models.TextField()
    score = models.IntegerField()
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
        return self.text


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
