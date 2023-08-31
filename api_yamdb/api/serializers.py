from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers

from reviews.models import Comment, Review


User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='author'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='title'
    )

    class Meta:
        model = Review
        fields = '__all__'
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Повторная отпрвка невозможна.'
            ), )

    def validate_score(self, value):
        if value not in settings.SCORE_RANGE:
            raise serializers.ValidationError(
                'Используйте оценку от 1 до 10!')
        return value
