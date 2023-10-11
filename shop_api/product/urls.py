from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list_create_api_view),
    path('products/<int:id>/', views.product_item_update_delete_api_view),
    path('products/reviews/', views.product_reviews_api_view),
    path('category/', views.category_list_create_api_view),
    path('category/<int:id>/', views.category_item_update_delete_api_view),
    path('reviews/', views.review_list_create_api_view),
    path('reviews/<int:id>/', views.review_item_update_delete_api_view),
]