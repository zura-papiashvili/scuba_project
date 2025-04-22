from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import JsonResponse
from users.models import User
from trips.models import DivingTrip as Trip, Location
from courses.models import Course


from django.core.mail import send_mail

# Create your views here.


class LandingPageView(TemplateView):
    template_name = "landing/landing_page.html"
    trips = Trip.objects.all()[:3]
    locations = Location.objects.all()[:3]
    courses = Course.objects.all()[:3]
    instructors = User.objects.filter(groups__name="Instructor")[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trips"] = self.trips
        context["locations"] = self.locations
        context["courses"] = self.courses
        context["instructors"] = self.instructors

        # Fetch data from other apps' models and add to context
        return context


class AboutView(TemplateView):
    instructors = User.objects.filter(groups__name="Instructor")
    template_name = "landing/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["instructors"] = self.instructors
        return context


def contact(request):
    if request.method == "POST":
        message_name = request.POST.get("message-name")
        message_email = request.POST.get("message-email")
        message = request.POST.get("message")

        # Send the email
        email_message = render_to_string(
            "email/contact_email.html",  # Template for email content
            {
                "message_name": message_name,
                "message_email": message_email,
                "message": message,
            },
        )

        try:
            send_mail(
                f"Message from {message_name}",
                "",  # No plain text message
                message_email,
                [settings.EMAIL_HOST_USER],
                html_message=email_message,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Error sending message: {e}")

        # Print to check if messages are set
        print(messages.get_messages(request))

        return render(request, "landing/contact.html", {"message_name": message_name})

    return render(request, "landing/contact.html")


def keep_warm(request):
    """Simple endpoint to keep the serverless function warm"""
    return JsonResponse({"status": "OK", "message": "Server is warm!"})


import os
import asyncio
import edge_tts
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render


async def generate_voice(text, voice, filename):
    """Generate TTS audio and save it to a file"""
    # Initialize the Communicate object
    communicate = edge_tts.Communicate(text, voice)

    try:
        # Open a file for saving the audio
        with default_storage.open(filename, "wb") as f:
            # Stream the audio content and write it to the file
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
    except Exception as e:
        raise Exception(f"Error while writing to file: {str(e)}")

    return filename


async def tts_view(request):
    if request.method == "POST":
        # Get the text and voice from the POST data
        text = request.POST.get("text")
        voice = request.POST.get("voice")

        # Ensure text and voice are provided
        if not text or not voice:
            return JsonResponse({"error": "Missing text or voice"}, status=400)

        try:
            # Create a unique filename
            filename = f"media/{voice}_{text[:5]}.mp3"

            # Generate speech and save it asynchronously
            file_path = await generate_voice(text, voice, filename)

            # Assuming the media is hosted via S3
            audio_url = f"https://zpscuba.s3.us-west-1.amazonaws.com/media/{file_path}"
            return JsonResponse({"audio_url": audio_url})

        except Exception as e:
            return JsonResponse(
                {"error": f"Failed to generate audio: {str(e)}"}, status=500
            )

    # If GET request, render the form
    return render(request, "landing/tts.html")
