from django.urls import path
from .views import product_api

urlpatterns = [
    path('products/', product_api),
    path('products/<int:pk>/', product_api),
]