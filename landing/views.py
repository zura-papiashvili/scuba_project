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


class ContactView(FormView):
    template_name = "landing/contact.html"
    form_class = ContactForm
    success_url = "/contact/"  # Redirect to the contact page after submission

    def form_valid(self, form):
        # Retrieve form data
        message_name = form.cleaned_data["message_name"]
        message_email = form.cleaned_data["message_email"]
        message = form.cleaned_data["message"]

        # Create a nicely formatted HTML message
        email_message = render_to_string(
            "email/contact_email.html",  # Email content template
            {
                "message_name": message_name,
                "message_email": message_email,
                "message": message,
            },
        )

        try:
            # Send the email
            send_mail(
                f"Message from {message_name}",  # Subject
                "",  # No plain text message
                message_email,  # From email
                [settings.EMAIL_HOST_USER],  # To email
                html_message=email_message,  # HTML message content
            )
            # Show success message
            messages.success(self.request, "Your message has been sent successfully!")
        except Exception as e:
            # Show error message
            messages.error(self.request, f"Error sending message: {e}")

        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle invalid form submission
        messages.error(
            self.request, "There was an error with your form. Please try again."
        )
        return super().form_invalid(form)
