from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, Category, Review, Tag


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = Product
        fields = 'id title description price category tags'.split()


class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True)

    class Meta:
        model = Product
        fields = 'title rating reviews'.split()


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=30)
    description = serializers.CharField(required=False)
    price = serializers.FloatField(min_value=20)
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField(max_value=1))

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exists')
        return category_id

    def validate_tags(self, tags):
        tags_db = Tag.objects.filter(id__in=tags)
        if len(tags_db) != len(tags):
            tags_db_ids = set(tag.id for tag in tags_db)
            diff_values = [tag_id for tag_id in tags if tag_id not in tags_db_ids]
            raise ValidationError(f"Tags doesn't exists: {diff_values}")
        return tags


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField(min_value=1)

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exists')
        return product_id
