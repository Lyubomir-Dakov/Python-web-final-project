from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.db.models import Q
from django.utils.text import slugify

UserModel = get_user_model()


class Car(models.Model):
    TYPE_CHOICES = (
        ('Sports Car', 'Sports Car'),
        ('Pickup', 'Pickup'),
        ('Crossover', 'Crossover'),
        ('Other', 'Other'),
    )
    TYPE_MAX_LEN = 20

    MODEL_MAX_LEN = 20
    MODEL_MIN_LEN = 2

    YEAR_OF_PRODUCTION_VERBOSE_NAME = 'Year of production'
    YEAR_MIN_VALUE = 1980
    YEAR_VALIDATION_ERROR_MESSAGE = 'This car is too old!'

    IMAGE_URL_VERBOSE_NAME = 'Image URL'

    PRICE_MIN_VALUE = 30000
    PRICE_VALIDATION_ERROR_MESSAGE = 'This car is too cheap to stay in the showroom!'

    HORSE_POWER_VERBOSE_NAME = 'Horse Power'
    HORSE_POWER_MIN_VALUE = 100
    HORSE_POWER_VALIDATION_ERROR_MESSAGE = 'This car is too weak to stay in the showroom!'

    type = models.CharField(
        max_length=TYPE_MAX_LEN,
        choices=TYPE_CHOICES,
        null=False,
        blank=False,
    )

    model = models.CharField(
        max_length=MODEL_MAX_LEN,
        validators=(
            MinLengthValidator(MODEL_MIN_LEN),
        ),
        null=False,
        blank=False,
    )

    year_of_production = models.PositiveIntegerField(
        verbose_name=YEAR_OF_PRODUCTION_VERBOSE_NAME,
        validators=(
            MinValueValidator(YEAR_MIN_VALUE, message=YEAR_VALIDATION_ERROR_MESSAGE),
        ),
        null=False,
        blank=False,
    )

    image_url = models.URLField(
        verbose_name=IMAGE_URL_VERBOSE_NAME,
        null=False,
        blank=False,
    )

    price = models.FloatField(
        validators=(
            MinValueValidator(PRICE_MIN_VALUE, message=PRICE_VALIDATION_ERROR_MESSAGE),
        ),
        null=False,
        blank=False,
    )

    horse_power = models.PositiveIntegerField(
        verbose_name=HORSE_POWER_VERBOSE_NAME,
        validators=(
            MinValueValidator(HORSE_POWER_MIN_VALUE, message=HORSE_POWER_VALIDATION_ERROR_MESSAGE),
        )
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=True
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.id}-{self.model}')

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.model

