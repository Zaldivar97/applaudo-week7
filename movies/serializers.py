from rest_framework import serializers

from .models import Movie, Category
from applaudo_week7.settings import BASE_API_URI


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'url'
        ]

    def get_url(self, obj):
        return BASE_API_URI + 'categories/'


class MovieSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'description',
            'stock',
            'available',
            'price',
            'active',
            'register_date',
            'rents',
            'url',
            'categories',
        ]
        # read_only_fields = ['cat']

    def get_url(self, obj):
        return BASE_API_URI + 'movies/'
