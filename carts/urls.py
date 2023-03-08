from django.urls import path
from . import views

urlpatterns = [
    path('cart/<int:product_id>/', views.ProductToCartView.as_view()),
    path('cart/', views.CartView.as_view())
]
