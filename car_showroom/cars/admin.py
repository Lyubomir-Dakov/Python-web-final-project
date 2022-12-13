from django.contrib import admin

from car_showroom.cars.models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('user', 'model', 'horse_power', 'price')
    ordering = ['-price']
    list_filter = ['user']
