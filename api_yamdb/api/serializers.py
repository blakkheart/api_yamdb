from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import (Comment, Review, Category, Genre, Title)


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Cannot use "me" as a name')
        return value

    def validate(self, data):
        if User.objects.filter(
            username=data.get('username'), email=data.get('email')
        ):
            return data
        elif User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Username has already been taken'
            )
        elif User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Email adress has already been taken'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    confirmation_code = serializers.CharField(required=True)


class UserEditSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)

    def validate(self, data):
        if User.objects.filter(
            username=data.get('username'), email=data.get('email')
        ):
            return data
        elif User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Username has already been taken'
            )
        elif User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Email adress has already been taken'
            )
        return data


class UserAdminEditSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate(self, data):
        if User.objects.filter(
            username=data.get('username'), email=data.get('email')
        ):
            return data
        elif User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Username has already been taken'
            )
        elif User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Email adress has already been taken'
            )
        return data


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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre', 'description')
