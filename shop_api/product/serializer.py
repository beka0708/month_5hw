from rest_framework import serializers
from .models import Product, Category, Review


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name products_count'.split()


class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text product stars'.split()


class ReviewItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = Product
        fields = 'id title description price category'.split()


class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True)

    class Meta:
        model = Product
        fields = 'title rating reviews'.split()


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

