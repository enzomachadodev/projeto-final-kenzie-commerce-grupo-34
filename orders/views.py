from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Order
from .serializers import OrderSerializer
from .permissions import IsCartNotEmptyOrReadOnly, IsSellerOrReadOnly


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCartNotEmptyOrReadOnly]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        cart = self.request.user.cart

        serializer.save(buyer=self.request.user, cart=cart)

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.filter(buyer_id=request.user.id)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


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
