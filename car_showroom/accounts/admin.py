from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from car_showroom.accounts.forms import AppUserCreationForm, UserEditForm
from car_showroom.accounts.models import CustomUser


UserModel = get_user_model()


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    add_form = AppUserCreationForm
    form = UserEditForm
    model = CustomUser
    ordering = ('email',)
    list_display = ('email', 'is_staff', 'is_active','last_login', 'is_superuser',)
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser',)}
         ),
    )
    search_fields = ('email',)

