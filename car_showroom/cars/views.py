from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from car_showroom.cars.forms import CarDetailsForm, CarEditForm, CarCreateForm, CarDeleteForm
from car_showroom.cars.models import Car
from car_showroom.cars.utils import get_car_by_model_and_user_id
from car_showroom.common.forms import CommentCarForm
from car_showroom.common.models import CarLike, CarTestDrive
from car_showroom.common.utils import user_has_test_drive_with_current_car

UserModel = get_user_model()


def car_details(request, slug, user_id):
    try:
        car = get_car_by_model_and_user_id(slug, user_id)
        user_has_test_drive = user_has_test_drive_with_current_car(user_id=request.user.pk, car_id=car.pk)
        user_like_cars = CarLike.objects.filter(car_id=car.pk, user_id=request.user.pk)

        context = {
            'car': car,
            'has_user_liked_car': user_like_cars,
            'is_owner': car.user == request.user,
            'likes_count': car.carlike_set.count(),
            'comment_form': CommentCarForm(),
            'user_has_test_drive': user_has_test_drive
        }

    except ObjectDoesNotExist as ex:
        return render(request, 'exception-handling/car-details-error-page.html')
    return render(request, 'cars/car-details-page.html', context)


def car_edit(request, slug, user_id):
    try:
        car = get_car_by_model_and_user_id(slug, user_id)

        if not car.user == request.user:
            return redirect('home page', user_id=user_id, slug=slug)

        if request.method == 'GET':
            form = CarEditForm(instance=car)
        else:
            form = CarEditForm(request.POST, instance=car)
            if form.is_valid():
                form.save()
                return redirect('car details', user_id=user_id, slug=slug)

        context = {
            'car': car,
            'form': form,
            'user_id': user_id,
        }

    except ObjectDoesNotExist as ex:
        return render(request, 'exception-handling/car-details-error-page.html')
    return render(request, 'cars/car-edit-page.html', context)


@login_required
def car_add(request):
    if request.method == 'GET':
        form = CarCreateForm()
    else:
        form = CarCreateForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()
            return redirect('home page')
    context = {
        'form': form,
    }
    return render(request, 'cars/car-add-page.html', context)


def car_delete(request, slug, user_id):
    try:
        car = get_car_by_model_and_user_id(slug, user_id)

        if not car.user == request.user:
            return redirect('home page')

        if request.method == 'GET':
            form = CarDeleteForm(instance=car)
        else:
            form = CarDeleteForm(request.POST, instance=car)
            if form.is_valid():
                form.save()
                return redirect('home page')

        context = {
            'form': form,
            'slug': slug,
            'user_id': user_id,
        }
    except ObjectDoesNotExist as ex:
        return render(request, 'exception-handling/car-details-error-page.html')
    return render(request, 'cars/car-delete-page.html', context)
