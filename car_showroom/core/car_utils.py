def apply_likes_count(car):
    car.likes_count = car.carlike_set.count()
    return car

#
# def apply_user_liked_car(car):
#     car.is_liked_by_user = car.likes_count > 0
#     return car
