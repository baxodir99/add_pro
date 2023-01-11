from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RegisterUserForm
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = RegisterUserForm
    model = User
    list_display = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'date_joined',
    ]
    search_fields = [
        'username',
        'email',
    ]
