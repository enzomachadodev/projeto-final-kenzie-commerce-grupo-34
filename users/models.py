from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True, max_length=50)
    photo_url = models.TextField(null=True)
    is_seller = models.BooleanField(default=False)
