from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import compress_and_optimize_image, validate_image_size
from django_countries.fields import CountryField

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    country = CountryField(blank_label="(Select country)", null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        default="images/profile-alt.png",
        blank=True,
        validators=[validate_image_size],
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="users_in_group",  # Change this to a unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="permissions_for_user",  # Change this to a unique related_name
        blank=True,
    )

    def __str__(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        if self.profile_picture:
            # Compress and optimize image before saving
            self.profile_picture = compress_and_optimize_image(self.profile_picture)
        super().save(*args, **kwargs)
