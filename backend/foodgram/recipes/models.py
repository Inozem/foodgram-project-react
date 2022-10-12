from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс пользователей"""
    email = models.EmailField(unique=True)
