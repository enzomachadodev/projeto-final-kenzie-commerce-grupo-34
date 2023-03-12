from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Product
from .permission import IsSellerOrAdminOrReadOnly
from .serializers import ProductSerializer


class ProductView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSellerOrAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductCategoryNameView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def filter_queryset(self, queryset):
        param1 = self.request.query_params.get("category", None)
        param2 = self.request.query_params.get("name", None)
        if param1:
            return queryset.filter(category=param1)
        elif param2:
            return queryset.filter(name=param2)
        else:
            return []


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSellerOrAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Create your views here.
