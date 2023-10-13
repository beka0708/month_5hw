from django.urls import path
from . import views

urlpatterns = [
    path('autorization/', views.AuthorizationAPIView.as_view()),
    path('registration/', views.RegistrationAPIView.as_view()),
    path('confirim/', views.ConfirmAPIViews.as_view()),
]
