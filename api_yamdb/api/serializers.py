from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = (Category, Genre, Title)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (Category, Genre, Title)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        fields = (Category, Genre, Title)
        model = Title
