from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'address', 'dob', 'is_active', 'is_staff']
    search_fields = ['email']
    list_filter = ['is_active']