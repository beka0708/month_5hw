from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list_api_view),
    path('products/<int:id>/', views.product_item__api_view),
    path('category/', views.category_list_api_view),
    path('category/<int:id>/', views.category_item_api_view),
    path('reviews/', views.review_list_api_view),
    path('reviews/<int:id>/', views.review_item_api_view),
]