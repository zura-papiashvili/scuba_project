from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .forms import ContactForm

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
    success_url = reverse_lazy("contact")  # Redirect to contact page after submission

    def form_valid(self, form):
        # Process the form (e.g., send an email, save data to the database, etc.)
        # You can access form.cleaned_data to get the form fields
        return super().form_valid(form)
