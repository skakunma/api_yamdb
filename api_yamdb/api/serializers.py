from rest_framework import serializers

from reviews.models import Comment, Review, User
from reviews.constants import MIN_SCORE, MAX_SCORE


class ReviewSerializer(serializers.ModelSerializer):
    """
    Класс ReviewSerializer.
    Класс ReviewSerializer описывает сериализатор
    отзывов.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        model = Review
        read_only_fields = ('author', 'title')

    def validate_score(self, value):
        if (MIN_SCORE <= value <= MAX_SCORE):
            return value
        raise serializers.ValidationError(
            'Оценка произведения модет быть от 1 до 10'
        )

    def validate(self, data):
        request = self.context['request']
        if request.method == "PATCH":
            return data
        author = request.user
        title = (
            request.parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(author=author, title=title):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Класс CommentSerializer.
    Класс CommentSerializer описывает сериализатор
    комментариев.
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment
