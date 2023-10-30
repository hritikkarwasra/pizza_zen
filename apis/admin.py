from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pizza._meta.fields]
    list_filter = ('base_type', 'cheese_type')
    search_fields = ('description',)
    filter_horizontal = ('toppings',)


@admin.register(Topping)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
