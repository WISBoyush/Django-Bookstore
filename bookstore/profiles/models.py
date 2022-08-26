from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import User
from datetime import date


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Biographic'
    )

    date_of_birth = models.DateField(
        "Date of birth",
        null=True,
        blank=True,
        auto_now=False,
        auto_now_add=False,
        default=date.today
    )

    phone = models.CharField(
        validators=[RegexValidator(r'\d{11}', 'Minimum 11', code='invalid')],
        verbose_name='Phone',
        max_length=18
    )

    balance = models.IntegerField(default=0)

    person_disc = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.email)
