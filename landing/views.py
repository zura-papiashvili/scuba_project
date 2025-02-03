from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render


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
        message_name = request.POST["message-name"]
        message_email = request.POST["message-email"]
        message = request.POST["message"]

        # Create a nicely formatted HTML message
        email_message = render_to_string(
            "email/contact_email.html",  # Create a new template for email content
            {
                "message_name": message_name,
                "message_email": message_email,
                "message": message,
            },
        )

        send_mail(
            f"Message from {message_name}",  # Subject
            "",  # No plain text message
            message_email,  # From email
            [settings.EMAIL_HOST_USER],  # To email
            html_message=email_message,  # HTML message content
        )

        return render(request, "landing/contact.html", {"message_name": message_name})

    return render(request, "landing/contact.html", {})
