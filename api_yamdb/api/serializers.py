import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.mixins import UserMixinSerializer
from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class UserCreateSerializer(UserMixinSerializer):
    """Serializer for {User} model for auth/signup/ adress.
    Inherites from {UserMixinSerializer}.
    Validates {username} not allowing to register with 'me' as username.
    Validates {username} and {email} not allowing to register user
        via someone elses username and email.
    """

    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Cannot use "me" as a name')
        return value


class TokenSerializer(serializers.Serializer):
    """Serializer for {Token} for auth/token/ adress."""

    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    confirmation_code = serializers.CharField(required=True)


class UserEditSerializer(UserMixinSerializer):
    """Serializer for {User} model for /users/ adress.
    Inherits from {UserMixinSerializer}.
    Validates {username} and {email} not allowing to get accesses to data
        via someone elses username and email.
    """

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


class UserAdminEditSerializer(UserMixinSerializer):
    """Serializer for {User} model for /users/ adress.
    Inherits from {UserMixinSerializer}.
    Validates {username} and {email} not allowing to get accesses to data
        via someone elses username and email.
    """

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


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for {Comment} model."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for {Review} model.
    Validates {score} field not allowing to add score outside of [1,10] range.
    Validates {author} and {title_id} not allowing to
        post review twice for the same title.
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        """Validates {score} field not allowing
            to add score outside of [1,10] range.
        """
        if value not in settings.SCORE_RANGE:
            raise serializers.ValidationError(
                'Choose the number between 1 and 10'
            )
        return value

    def validate(self, data):
        """Validates {author} and {title_id} not allowing to
            post review twice for the same title.
        """
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(
                author=self.context.get('request').user,
                title=self.context.get('view').kwargs.get('title_id'),
            ):
                raise serializers.ValidationError(
                    'Cannot review same title twice'
                )
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for {Category} model."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for {Genre} model."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for {Title} model if request.method!=GET.
    Validates {year} field not allowing to add a future year.
    """

    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, read_only=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def validate_year(self, value):
        """Validates {year} field not allowing to add a future year."""
        if value > datetime.date.today().year:
            return serializers.ValidationError('Cannot add a future year')
        return value


class GetTitleSerializer(serializers.ModelSerializer):
    """Serializer for {Title} model if request.method=GET."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
