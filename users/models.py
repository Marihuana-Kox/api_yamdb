from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    bio = models.TextField(blank=True)
    ROLES = (("user", "user"), ("moderator", "moderator"), ("admin", "admin"))

    role = models.CharField(max_length=9, choices=ROLES, default="user")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
