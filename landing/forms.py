from django import forms


class ContactForm(forms.Form):
    message_name = forms.CharField(max_length=100, label="Your Name")
    message_email = forms.EmailField(label="Your Email")
    message = forms.CharField(widget=forms.Textarea, label="Message")
