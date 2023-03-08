from .serializers import CartSerializer
from rest_framework.views import Response, status
from rest_framework import generics
from .models import Cart
from products.models import Product, CartProducts
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import ipdb


class ProductToCartView(generics.CreateAPIView, generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    lookup_field = "product_id"

    def create(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        cart = get_object_or_404(Cart, buyer_id=request.user.id)

        product_exist = CartProducts.objects.filter(cart_id=cart.id, product_id=product).first()

        if product_exist:
            product_exist.quantity += 1
            product_exist.save()
        else:
            cart.products.add(product)
        serializer = CartSerializer(cart)

        return Response(serializer.data, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        cart = get_object_or_404(Cart, buyer_id=request.user.id)
        product = cart.products.filter(id=product_id).first()
        cart.products.remove(product)
        serializer = CartSerializer(cart)

        return Response(serializer.data, status.HTTP_200_OK)


class CartView(generics.ListAPIView, generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, buyer_id=request.user.id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, buyer_id=request.user.id)
        cart.products.clear()
        serializer = CartSerializer(cart)

        return Response(serializer.data, status.HTTP_200_OK)
