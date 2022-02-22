from django.contrib.auth.models import AbstractUser
from django.db import models


class Provider(AbstractUser):
    email = models.EmailField()
    phone_number = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.username
