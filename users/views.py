from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import UserSerializer


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_url_kwarg = "user_id"
