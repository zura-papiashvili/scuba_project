from django.urls import path
from .views import (
    TripListView,
    TripDetailView,
    BookingCreateView,
    EquipmentRentalCreateView,
    LocationMapView,
)


urlpatterns = [
    path("", TripListView.as_view(), name="trip_list"),
    path("<int:trip_id>/", TripDetailView.as_view(), name="trip_detail"),
    path("<int:trip_id>/book/", BookingCreateView.as_view(), name="book_trip"),
    path(
        "<int:trip_id>/rent-equipment/",
        EquipmentRentalCreateView.as_view(),
        name="rent_equipment",
    ),
    path("map/", LocationMapView.as_view(), name="map"),
]
