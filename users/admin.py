from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "country",
        "phone_number",
        "biography",
    )
    search_fields = ["username", "email", "first_name", "last_name"]
    list_filter = ["country"]
