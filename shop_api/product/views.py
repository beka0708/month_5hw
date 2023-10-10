from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Category, Review
from .serializer import ProductListSerializer, CategoryListSerializer, ReviewListSerializer, \
    ProductItemSerializer, CategoryItemSerializer, ReviewItemSerializer, ProductReviewsSerializer


@api_view(['GET'])
def product_list_api_view(request):
    product = Product.objects.all()
    data = ProductListSerializer(instance=product, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_reviews_api_view(request):
    product = Product.objects.all()
    data = ProductReviewsSerializer(instance=product, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_item__api_view(request, id):
    try:
        item_product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'errors': 'Product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductItemSerializer(instance=item_product, many=False).data
    return Response(data=data)


@api_view(['GET'])
def category_list_api_view(request):
    category = Category.objects.all()
    data = CategoryListSerializer(instance=category, many=True).data
    return Response(data=data)


@api_view(['GET'])
def category_item_api_view(request, id):
    try:
        item_category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = CategoryItemSerializer(instance=item_category, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_list_api_view(request):
    review = Review.objects.all()
    data = ReviewListSerializer(instance=review, many=True).data
    return Response(data=data)


@api_view(['GET'])
def review_item_api_view(request, id):
    try:
        item_review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewItemSerializer(instance=item_review, many=False).data
    return Response(data=data)
