# urls.py (inside the landing app)

from django.urls import path
from . import views

urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing_page"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]
