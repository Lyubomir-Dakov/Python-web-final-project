from django.contrib import admin

from car_showroom.common.models import CarComment, CarLike, CarTestDrive


@admin.register(CarComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'car', 'publication_date_and_time')
    list_filter = ('publication_date_and_time',)
    search_fields = ('user', 'car')


@admin.register(CarTestDrive)
class TestDriveCarAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'test_drive_date')


@admin.register(CarLike)
class CarLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'car',)
