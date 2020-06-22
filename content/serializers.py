from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Review

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["name", "slug"]
        model = Category


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:

        fields = ["name", "slug"]
        model = Genre


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreField(
        slug_field="slug", required=False, many=True, queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field="slug", required=False, queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:

        fields = ["id", "name", "year", "description", "genre", "category", "rating"]
        model = Title

    def get_rating(self, value):

        rating = Review.objects.filter(title=value).aggregate(Avg("score"))
        return rating["score__avg"]
