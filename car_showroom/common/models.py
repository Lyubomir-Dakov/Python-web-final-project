import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from car_showroom.cars.models import Car

UserModel = get_user_model()


class CarLike(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        null=False,
        blank=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class CarComment(models.Model):
    CAR_COMMENT_VERBOSE_NAME = ''
    MAX_TEXT_LENGTH = 100
    text = models.CharField(
        verbose_name=CAR_COMMENT_VERBOSE_NAME,
        max_length=MAX_TEXT_LENGTH,
        null=False,
        blank=False,
    )

    publication_date_and_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['publication_date_and_time']


class CarTestDrive(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    test_drive_date = models.DateField(
        verbose_name='Test drive date',
        default=datetime.datetime.now(),
        null=False,
        blank=False
    )

    def save(self, *args, **kwargs):
        if self.test_drive_date < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")
        super(CarTestDrive, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} want to test {self.car.model}'

    class Meta:
        ordering = ['test_drive_date']
