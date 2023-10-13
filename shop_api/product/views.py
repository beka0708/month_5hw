from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Product, Category, Review
from .serializer import ProductListSerializer, CategoryListSerializer, ReviewListSerializer, \
    ProductItemSerializer, CategoryItemSerializer, ProductReviewsSerializer, \
    ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer, ReviewItemSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
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


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductItemSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        try:
            item_product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(data={'errors': 'Product not found'},
                            status=status.HTTP_404_NOT_FOUND)

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


class ProductReviewsAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductReviewsSerializer
    pagination_class = PageNumberPagination


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
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


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryItemSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        try:
            item_category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response(data={'error': 'Not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        item_category.name = serializer.validated_data.get('name')
        item_category.save()
        return Response(data=CategoryItemSerializer(item_category).data,
                        status=status.HTTP_202_ACCEPTED)


class ReviewsListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
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


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewItemSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        try:
            item_review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response(data={'error': 'Not found'},
                            status=status.HTTP_404_NOT_FOUND)

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

