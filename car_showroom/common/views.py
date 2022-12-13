from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic as views

from car_showroom.cars.models import Car
from car_showroom.common.forms import SearchCarsByTypeForm, CommentCarForm, CreateTestDriveForm, EditTestDriveForm, \
    DeleteTestDriveForm
from car_showroom.common.models import CarLike, CarComment, CarTestDrive
from car_showroom.common.utils import get_car_url


def index(request):
    search_form = SearchCarsByTypeForm(request.GET)
    search_pattern = None
    cars = Car.objects.all()

    if search_form.is_valid():
        search_pattern = search_form.cleaned_data['car_type']

    if search_pattern:
        cars = cars.filter(type__icontains=search_pattern)

    paginator = Paginator(cars, 2)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context = {
        'cars': cars,
        'search_form': search_form,
        'page_object': page_object,
        'car_list': cars
    }
    return render(request, 'common/home-page.html', context)


def about(request):
    return render(request, 'base/partials/about-page.html')


@login_required
def like_car(request, car_id):
    current_user_liked_this_car = CarLike.objects \
        .filter(car_id=car_id, user_id=request.user.pk)

    if current_user_liked_this_car:
        current_user_liked_this_car.delete()
    else:
        CarLike.objects.create(
            car_id=car_id,
            user_id=request.user.pk,
        )

    return redirect(get_car_url(request, car_id))


@login_required
def comment_car(request, car_id):
    car = Car.objects.filter(pk=car_id).get()
    form = CommentCarForm(request.POST)

    if form.is_valid():
        text = request.POST.get('text')
        comment = CarComment.objects.create(car=car, user_id=request.user.pk, text=text)
        comment.save()

    return redirect('car details', slug=car.slug, user_id=car.user.pk)


@login_required
def test_drive_car(request, car_id):
    try:

        car = Car.objects.filter(pk=car_id).get()

        if request.method == 'GET':
            form = CreateTestDriveForm()
        else:
            form = CreateTestDriveForm(request.POST)
            if form.is_valid():
                test_drive = form.save(commit=False)
                test_drive.user = request.user
                test_drive.car = car
                test_drive.save()
                return redirect('car details', slug=car.slug, user_id=car.user.pk)

        context = {
            'form': form,
            'car': car,
        }
    except ObjectDoesNotExist:
        return render(request, 'exception-handling/test-drive-error-page.html')

    return render(request, 'common/test-drive-page.html', context)


@login_required
def edit_test_drive(request, car_id):
    try:

        car = Car.objects.filter(pk=car_id).get()
        current_test_drive = CarTestDrive.objects.get(car_id=car_id, user_id=request.user.pk)

        if request.method == 'GET':
            form = EditTestDriveForm(instance=current_test_drive)
        else:
            form = EditTestDriveForm(request.POST, instance=current_test_drive)
            if form.is_valid():
                form.save()
                return redirect('car details', slug=car.slug, user_id=car.user.pk)
        context = {
            'form': form,
            'car': car,
        }

    except ObjectDoesNotExist:
        return render(request, 'exception-handling/test-drive-error-page.html')
    return render(request, 'common/edit-test-drive-page.html', context)


@login_required
def del_test_drive(request, car_id):
    try:
        car = Car.objects.filter(pk=car_id).get()
        current_test_drive = CarTestDrive.objects.get(car_id=car_id, user_id=request.user.pk)

        if request.method == 'GET':
            form = DeleteTestDriveForm(instance=current_test_drive)
        else:
            form = DeleteTestDriveForm(request.POST, instance=current_test_drive)
            if form.is_valid():
                form.save()
                return redirect('car details', slug=car.slug, user_id=car.user.pk)
        context = {
            'form': form,
            'car': car,
        }
    except ObjectDoesNotExist:
        return render(request, 'exception-handling/test-drive-error-page.html')

    return render(request, 'common/delete-test-drive-page.html', context)
