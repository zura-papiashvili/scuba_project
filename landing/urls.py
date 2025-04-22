# urls.py (inside the landing app)

from django.urls import path
from . import views

urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing_page"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.contact, name="contact"),
    path("keep-warm/", views.keep_warm, name="keep_warm"),
    path("voices/", views.tts_view, name="tts_view"),
]
