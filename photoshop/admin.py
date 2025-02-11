from django.contrib import admin
from .models import ProcessedImage


# Register your models here.
@admin.register(ProcessedImage)
class ProcessedImageAdmin(admin.ModelAdmin):
    list_display = ("user", "work_url", "photo_name")
