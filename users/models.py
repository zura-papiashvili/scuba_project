from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import compress_and_optimize_image, validate_image_size

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
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
        return self.username

    def save(self, *args, **kwargs):
        if self.image:
            # Compress and optimize image before saving
            self.image = compress_and_optimize_image(self.image)
        super().save(*args, **kwargs)
