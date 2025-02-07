from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Course


@admin.register(Course)
class CourseAdmin(TranslationAdmin):
    list_display = ("name", "price", "duration")
