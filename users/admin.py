from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.fields import GenericIPAddressField
from. import models # . -> 같은 폴더 내에있는 models를 import


@admin.register(models.User) # == admin.site.register(models.User, CustomUserAdmin)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Profile", {"fields": ("avatar", "gender", "bio" ,"birthday","language","currency", "superhost",       
                )
            }
        ),
    )
    list_filter = UserAdmin.list_filter+("superhost",)
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )