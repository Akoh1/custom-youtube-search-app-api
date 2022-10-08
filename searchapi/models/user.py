from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

# Create your models here.
from rest_framework.authentication import TokenAuthentication

class BearerTokenAuth(TokenAuthentication):
    keyword = "Bearer"


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []



# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
