from django.contrib.auth import get_user_model
from car_showroom.cars.models import Car

UserModel = get_user_model()


def get_car_by_model_and_user_id(car_slug, user_id):
    return Car.objects.filter(slug=car_slug, user__id=user_id).get()


