from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .manager import UserManager


class User(AbstractUser):

    username = None
    email = models.EmailField(_("email address"), max_length=150, unique=True, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    first_name = None
    last_name = None


    objects = UserManager()

    def __str__(self):
        return self.email
