from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from os import path
import uuid


class CustomUser(AbstractUser):
    uuid = models.UUIDField(max_length=190, default=uuid.uuid4, editable=False, unique=True)
    address = models.CharField(max_length=200)
    # pincode = models.CharField(max_length=10)
    # full_name = models.CharField(max_length=200)


class OtpCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.code
