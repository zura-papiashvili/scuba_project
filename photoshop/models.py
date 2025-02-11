from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ProcessedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_url = models.URLField(blank=True, null=True, default="https://example.com")
    photo_name = models.CharField(max_length=255, default="default_image.jpg")

    def __str__(self):
        return self.photo_name
