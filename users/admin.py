from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "first_name",
        "last_name",
        "country",
        "phone_number",
        "biography",
        "profile_picture",
    )
    search_fields = ["username", "email", "first_name", "last_name"]
    list_filter = ["country"]


admin.site.register(User, CustomUserAdmin)
