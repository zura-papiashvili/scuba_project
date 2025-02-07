from django.db import models
from django.contrib.auth import get_user_model
from users.utils import compress_and_optimize_image, validate_image_size
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    instructor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="courses"
    )
    image = models.ImageField(
        upload_to="course_images/",
        blank=True,
        null=True,
        validators=[validate_image_size],
    )

    def save(self, *args, **kwargs):
        if self.image:
            # Compress and optimize image before saving
            self.image = compress_and_optimize_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("Ongoing", _("Ongoing")),
        ("Completed", _("Completed")),
        ("Dropped", _("Dropped")),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("Pending", _("Pending")),
        ("Paid", _("Paid")),
        ("Refunded", _("Refunded")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Ongoing")
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="Pending"
    )

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"
