from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from rest_framework import generics, status
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Order
from .serializers import OrderSerializer
from .permissions import IsCartNotEmptyOrReadOnly, IsSellerOrReadOnly, IsProductAvailableOrReadOnly
import ipdb


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCartNotEmptyOrReadOnly, IsProductAvailableOrReadOnly]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        cart = self.request.user.cart
        return serializer.save(buyer=self.request.user, cart=cart)

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.filter(buyer_id=request.user.id)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        resp = {"orders": []}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        for obj in objs:
            serializer = OrderSerializer(obj)
            resp["orders"].append(serializer.data)
        return Response(resp, status=status.HTTP_201_CREATED, headers=headers)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSellerOrReadOnly]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    lookup_url_kwarg = "order_id"

    def list(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.lookup_url_kwarg)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
