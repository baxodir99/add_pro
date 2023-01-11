from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    model = Business
    list_display = [
        'id',
        'name',
        'user',
        'created_at',
        'updated_at',
    ]
    search_fields = [
        'name'
    ]

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    model = Income
    list_display = [
        'id',
        'income',
        'customer_count',
        'month',
        'business',
        'created_at',
        'updated_at',
    ]

@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    model = Outcome
    list_display = [
        'id',
        'salary',
        'marketing',
        'month',
        'business',
        'created_at',
        'updated_at',
    ]

