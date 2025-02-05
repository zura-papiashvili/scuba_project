from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import JsonResponse


from django.core.mail import send_mail

# Create your views here.


class LandingPageView(TemplateView):
    template_name = "landing/landing_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch data from other apps' models and add to context
        return context


class AboutView(TemplateView):
    template_name = "landing/about.html"


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
