from django.urls import path, include

from car_showroom.cars.views import car_details, car_edit, car_delete, car_add

urlpatterns = (
    path('add/', car_add, name='car add'),
    path('<slug:slug>/<int:user_id>/', include([
        path('', car_details, name='car details'),
        path('edit/', car_edit, name='car edit'),
        path('delete/', car_delete, name='car delete'),
    ])),
)
