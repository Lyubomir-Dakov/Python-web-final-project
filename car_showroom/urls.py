from django.contrib import admin
from django.urls import path, include

# from car_showroom.core.exeption_handler import page_not_found_handler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('car_showroom.common.urls')),
    path('accounts/', include('car_showroom.accounts.urls')),
    path('cars/', include('car_showroom.cars.urls')),
]


# handler_404 = page_not_found_handler
# handler500 = handler500