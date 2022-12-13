from car_showroom.common.models import CarTestDrive


def get_car_url(request, car_id):
    return request.META['HTTP_REFERER'] + f'#car-{car_id}'


def user_has_test_drive_with_current_car(user_id, car_id):
    all_test_drives = CarTestDrive.objects.all()
    if all_test_drives:
        for test_drive in all_test_drives:
            if test_drive.user.pk == user_id and test_drive.car.pk == car_id:
                return False
        return True
    return True
