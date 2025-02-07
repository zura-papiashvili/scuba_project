from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from .models import DivingTrip, Booking, EquipmentRental, Equipment

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
