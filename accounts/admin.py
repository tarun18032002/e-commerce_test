from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','user_name','last_login','is_active','is_staff',)
    ordering = ('-date_joined',)
    list_display_links = ('email','first_name','last_name',)
    search_fields = ('email','first_name','last_name','user_name',)
    list_filter = ('is_active','is_staff',)
    readonly_fields = ('last_login','date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = () 

admin.site.register(Account,AccountAdmin)