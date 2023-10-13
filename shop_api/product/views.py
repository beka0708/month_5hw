from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Category, Review
from .serializer import ProductListSerializer, CategoryListSerializer, ReviewListSerializer, \
    ProductItemSerializer, CategoryItemSerializer, ReviewItemSerializer, ProductReviewsSerializer, \
    ProductValidateSerializer, ReviewValidateSerializer, CategoryValidateSerializer


@api_view(['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        data = ProductListSerializer(instance=product, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')

        product = Product.objects.create(
            title=title, description=description,
            price=price, category_id=category_id,
        )
        product.tags.set(tags)

        return Response(status=status.HTTP_201_CREATED,
                        data=ProductItemSerializer(product).data)


@api_view(['GET'])
def product_reviews_api_view(request):
    product = Product.objects.all()
    data = ProductReviewsSerializer(instance=product, many=True).data
    return Response(data=data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_item_update_delete_api_view(request, id):
    try:
        item_product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'errors': 'Product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductItemSerializer(instance=item_product, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        item_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        item_product.title = serializer.validated_data.get('title')
        item_product.description = serializer.validated_data.get('description')
        item_product.price = serializer.validated_data.get('price')
        item_product.category_id = serializer.validated_data.get('category_id')
        item_product.save()
        return Response(data=ProductItemSerializer(item_product).data,
                        status=status.HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        category = Category.objects.all()
        data = CategoryValidateSerializer(instance=category, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = CategoryListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        name = serializer.validated_data.get('name')
        category = Category.objects.create(
            name=name
        )
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryItemSerializer(category).data)


@api_view(['GET', 'PUT', 'DELETE'])
def category_item_update_delete_api_view(request, id):
    try:
        item_category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryItemSerializer(instance=item_category, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        item_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        item_category.name = serializer.validated_data.get('name')
        item_category.save()
        return Response(data=CategoryItemSerializer(item_category).data,
                        status=status.HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewListSerializer(instance=review, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        text = serializer.validated_data.get('text')
        product_id = serializer.validated_data.get('product_id')
        stars = serializer.validated_data.get('stars')

        review = Review.objects.create(
            text=text, stars=stars, product_id=product_id
        )

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewItemSerializer(review).data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_item_update_delete_api_view(request, id):
    try:
        item_review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewItemSerializer(instance=item_review, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        item_review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        item_review.text = request.data.get('text')
        item_review.product_id = request.data.get('product_id')
        item_review.stars = request.data.get('stars')
        item_review.save()
        return Response(data=ReviewItemSerializer(item_review).data,
                        status=status.HTTP_202_ACCEPTED)
