from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Product
from .serializers import ProductSerializer


class ProductView(generics.ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Create your views here.
