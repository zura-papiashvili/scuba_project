from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from .models import DivingTrip, Booking, EquipmentRental, Equipment, Location
import folium
from django.template.loader import render_to_string
from django.conf import settings

from django.contrib.auth.decorators import login_required


class TripListView(View):
    """Display all diving trips."""

    def get(self, request):
        trips = DivingTrip.objects.all()
        return render(request, "trips/trip_list.html", {"trips": trips})


class TripDetailView(View):
    """Display detailed information about a specific trip."""

    def get(self, request, trip_id):
        trip = get_object_or_404(DivingTrip, id=trip_id)
        locations = trip.location
        print(locations)
        return render(request, "trips/trip_detail.html", {"trip": trip})


class BookingCreateView(View):
    """Create a booking for a diving trip."""

    @login_required
    def post(self, request, trip_id):
        trip = get_object_or_404(DivingTrip, id=trip_id)
        num_people = int(request.POST.get("num_people", 1))
        total_price = trip.price * num_people

        booking = Booking.objects.create(
            user=request.user,
            trip=trip,
            num_people=num_people,
            total_price=total_price,
            payment_status="Pending",  # Assuming payment is handled elsewhere
            status="Pending",
        )
        return redirect("trips:trip_detail", trip_id=trip.id)


class EquipmentRentalCreateView(View):
    """Create an equipment rental for a diving trip."""

    @login_required
    def post(self, request, trip_id):
        trip = get_object_or_404(DivingTrip, id=trip_id)
        equipment_id = request.POST.get("equipment_id")
        rental_days = int(request.POST.get("rental_days", 1))
        equipment = get_object_or_404(Equipment, id=equipment_id)
        total_price = rental_days * equipment.rental_price_per_day

        rental = EquipmentRental.objects.create(
            user=request.user,
            trip=trip,
            equipment=equipment,
            rental_days=rental_days,
            total_price=total_price,
        )
        return redirect("trips:trip_detail", trip_id=trip.id)


class LocationMapView(View):
    """Display a map with all locations."""

    def get(self, request):
        # Retrieve all locations from the database
        locations = Location.objects.all()

        if locations:
            # Center the map based on the average latitude and longitude of all locations
            avg_lat = sum([loc.latitude for loc in locations]) / len(locations)
            avg_lon = sum([loc.longitude for loc in locations]) / len(locations)

            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=8)

            # Loop through each location and add a marker
            for location in locations:
                # Main location marker
                folium.Marker(
                    location=[location.latitude, location.longitude],
                    popup=location.name,
                ).add_to(m)

                # Define some offset values for the small pins
                offsets = [
                    (0.0003, 0.0003),  # Top-right
                    (0.0003, -0.0003),  # Top-left
                    (-0.0003, 0.0003),  # Bottom-right
                    (-0.0003, -0.0003),  # Bottom-left
                    (0.0005, 0),  # Above
                    (-0.0005, 0),  # Below
                ]

                # Create small markers around the main marker for each marine life
                for i, marine in enumerate(location.marine_life.all()):
                    if marine.image:
                        image_url = marine.image.url
                        # Calculate the offset position for this small marker
                        offset_lat, offset_lon = offsets[
                            i % len(offsets)
                        ]  # Cycle through offsets

                        html = f"""
                                <div style="
                                    background: url('{image_url}') no-repeat center center;
                                    background-size: cover;
                                    width: 40px;
                                    height: 40px;
                                    border-radius: 50%;
                                    border: 2px solid white;
                                    box-shadow: 0px 0px 5px rgba(0,0,0,0.5);
                                "></div>
                                """
                        # Add a small marker with the image
                        folium.Marker(
                            location=[
                                float(location.latitude) + float(offset_lat),
                                float(location.longitude) + float(offset_lon),
                            ],
                            icon=folium.DivIcon(html=html),
                            popup=render_to_string(
                                "trips/map_popup_content.html",
                                {
                                    "location": location,
                                    "marine_life": [marine],
                                },  # Pass list of marine life
                            ),
                        ).add_to(m)

            # Save the map as an HTML string
            map_html = m._repr_html_()

            # Pass the map HTML to the template
            return render(
                request,
                "trips/locations_map.html",
                {"map_html": map_html, "locations": locations},
            )
        else:
            return render(
                request, "trips/locations_map.html", {"error": "No locations found"}
            )
