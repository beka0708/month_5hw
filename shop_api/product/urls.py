from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<int:id>/', views.ProductDetailAPIView.as_view()),
    path('products/reviews/', views.ProductReviewsAPIView.as_view()),
    path('category/', views.CategoryListCreateAPIView.as_view()),
    path('category/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('reviews/', views.ReviewsListCreateAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),
]