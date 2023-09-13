from django.urls import path
from ecommerce.user import views

urlpatterns = [
    path('register', views.CreateUserView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
]