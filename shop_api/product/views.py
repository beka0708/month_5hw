from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Category, Review
from .serializer import ProductListSerializer, CategoryListSerializer, ReviewListSerializer, \
    ProductItemSerializer, CategoryItemSerializer, ReviewItemSerializer, ProductReviewsSerializer


@api_view(['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        data = ProductListSerializer(instance=product, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')

        product = Product.objects.create(
            title=title, description=description,
            price=price, category_id=category_id
        )

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
        item_product.title = request.data.get('title')
        item_product.description = request.data.get('description')
        item_product.price = request.data.get('price')
        item_product.category_id = request.data.get('category_id')
        item_product.save()
        return Response(data=ProductItemSerializer(item_product).data,
                        status=status.HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        category = Category.objects.all()
        data = CategoryListSerializer(instance=category, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        name = request.data.get('name')
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
        item_category.name = request.data.get('name')
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
        text = request.data.get('text')
        product_id = request.data.get('product_id')
        stars = request.data.get('stars')

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
        item_review.text = request.data.get('text')
        item_review.product_id = request.data.get('product_id')
        item_review.stars = request.data.get('stars')
        item_review.save()
        return Response(data=ReviewItemSerializer(item_review).data,
                        status=status.HTTP_202_ACCEPTED)
