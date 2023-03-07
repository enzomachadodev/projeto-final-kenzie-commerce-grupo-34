from .serializer import CartSerializer
from rest_framework import generics
from .models import Cart


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
