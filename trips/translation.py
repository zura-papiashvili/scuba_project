from modeltranslation.translator import register, TranslationOptions
from .models import DivingTrip, Equipment, Location, MarineLife, TripImage, DivingTrip


# Marine Life Translation
@register(MarineLife)
class MarineLifeTranslationOptions(TranslationOptions):
    fields = ("name", "description")


# Trip Translation
@register(DivingTrip)
class TripTranslationOptions(TranslationOptions):
    fields = ("title", "description")


# Equipment Translation
@register(Equipment)
class EquipmentTranslationOptions(TranslationOptions):
    fields = ("name", "description")


# Location Translation
@register(Location)
class LocationTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
    )


#  trip image
@register(TripImage)
class TripImageTranslationOptions(TranslationOptions):
    fields = ("caption",)
