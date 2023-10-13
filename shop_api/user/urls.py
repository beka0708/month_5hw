from django.urls import path
from . import views

urlpatterns = [
    path('autorization/', views.authorization_api_view),
    path('registration/', views.registration_api_view),
    path('confirim/', views.confirm_api_view),
]
