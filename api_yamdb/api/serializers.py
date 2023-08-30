from django.contrib.auth import get_user_model
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


SCORE_RANGE = range()
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
            ), )

    def validate_score(self, value):
        if value not in SCORE_RANGE:
            raise serializers.ValidationError(
                'Используйте оценку от 1 до 10')
        return value
