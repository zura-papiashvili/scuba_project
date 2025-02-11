# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("process_image/", views.process_image, name="process_image"),
    path(
        "upload-processed-image/",
        views.create_processed_image,
        name="create_processed_image",
    ),
    path(
        "user_processed_images/",
        views.user_processed_images,
        name="user_processed_images",
    ),
]
