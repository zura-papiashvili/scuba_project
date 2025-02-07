from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from users.utils import compress_and_optimize_image, validate_image_size


User = get_user_model()


class MarineLife(models.Model):
    """Model to represent marine life species."""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="marine_life_images/",
        validators=[validate_image_size],
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_and_optimize_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Location(models.Model):
    """Model for dive locations."""

    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    difficulty_level = models.CharField(
        max_length=50,
        choices=[
            ("Beginner", _("Beginner")),
            ("Intermediate", _("Intermediate")),
            ("Advanced", _("Advanced")),
        ],
        default="Beginner",
    )

    best_season = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=[
            ("Spring", _("Spring")),
            ("Summer", _("Summer")),
            ("Autumn", _("Autumn")),
            ("Winter", _("Winter")),
        ],
    )

    marine_life = models.ManyToManyField(MarineLife, blank=True)

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.country})"


class DivingTrip(models.Model):
    """Model for diving trips."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="trips"
    )
    date = models.DateField()
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_spots = models.PositiveIntegerField()
    instructor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="instructed_trips"
    )

    def __str__(self):
        return f"{self.title} - {self.date}"


class TripImage(models.Model):
    """Allows multiple images per trip."""

    trip = models.ForeignKey(
        DivingTrip, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="trip_images/", validators=[validate_image_size]
    )
    caption = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.image = compress_and_optimize_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.trip.title}"


class Booking(models.Model):
    """Stores user bookings for diving trips."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    trip = models.ForeignKey(
        DivingTrip, on_delete=models.CASCADE, related_name="bookings"
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    num_people = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    payment_status = models.CharField(
        max_length=50,
        choices=[("Paid", _("Paid")), ("Pending", _("Pending"))],
        default="Pending",
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", _("Pending")),
            ("Confirmed", _("Confirmed")),
            ("Cancelled", _("Cancelled")),
        ],
        default="Pending",
    )

    def save(self, *args, **kwargs):
        self.total_price = self.num_people * self.trip.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user} for {self.trip.title}"


class Equipment(models.Model):
    """List of available diving equipment."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    rental_price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(
        upload_to="equipment_images/",
        validators=[validate_image_size],
        blank=True,
        null=True,
    )
    condition = models.CharField(
        max_length=50,
        choices=[
            ("Good", _("Good")),
            ("Fair", _("Fair")),
            ("Poor", _("Poor")),
        ],
        default="Good",
    )
    available_quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_and_optimize_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.condition})"


class EquipmentRental(models.Model):
    """Stores rentals made by users for diving trips."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rentals")
    trip = models.ForeignKey(
        DivingTrip, on_delete=models.CASCADE, related_name="rentals"
    )
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="rentals"
    )
    rental_days = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.rental_days * self.equipment.rental_price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.equipment.name} for {self.user} on {self.trip.title}"
