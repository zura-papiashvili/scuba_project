from django.contrib import admin
from .models import Location, MarineLife, Equipment, TripImage, DivingTrip
from modeltranslation.admin import TranslationAdmin


@admin.register(MarineLife)
class MarineLifeAdmin(admin.ModelAdmin):
    list_display = ("name",)


class MarineLifeInline(admin.TabularInline):
    model = Location.marine_life.through
    extra = 1


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "difficulty_level", "best_season")
    search_fields = ("name", "country")
    inlines = [MarineLifeInline]


class TripImageInline(
    admin.TabularInline
):  # or use admin.StackedInline for a different layout
    model = TripImage
    extra = 1  # Allows adding one extra image by default


@admin.register(DivingTrip)
class TripAdmin(TranslationAdmin):
    list_display = ("title", "location", "date", "price")
    search_fields = ("title", "description")
    list_filter = ("location", "date")
    inlines = [TripImageInline]


@admin.register(Equipment)
class EquipmentAdmin(TranslationAdmin):
    list_display = ("name", "available_quantity")
    search_fields = ("name", "description")
