from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from car_showroom.accounts.managers import AppUserManager


class CustomUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        unique=True,
        null=False,
        blank=False,
    )

    is_staff = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )

    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = AppUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    FIRST_NAME_MAX_LEN = 30

    LAST_NAME_MAX_LEN = 30

    AGE_MIN_VALUE = 18

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
    )

    age = models.PositiveIntegerField(
        validators=(MinValueValidator(
            AGE_MIN_VALUE,
            message='You must be at least 18 years old!'),
        ),
        null=True,
        blank=True,
    )

    profile_picture = models.FileField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        CustomUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name

    def get_short_name(self):
        return self.first_name



