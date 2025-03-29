from django.contrib import admin
from .models import Products

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock','category', 'is_available', 'created_date', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Products, ProductsAdmin)