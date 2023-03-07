from django.urls import path
from . import views

urlpattenrs = [
    path('/<int:pk>/cart', views.CartView.as_view())
]
