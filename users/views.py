# views.py in your users app
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserSignupForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django_countries import countries


# Sign up view
def signup(request):
    # Directly pass the countries object to the template
    if request.method == "POST":
        form = UserSignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            messages.success(request, "Account created successfully!")
            return redirect("landing_page")  # Redirect to homepage or user dashboard
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(
                        f"Error in {field}: {error}"
                    )  # Keep for debugging in dev mode
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserSignupForm()

    # Render the signup form, passing country choices directly from django-countries
    return render(
        request,
        "users/signup.html",
        {
            "form": form,
            "countries": countries,  # Pass the countries directly
        },
    )


# Login view
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect("landing_page")  # Redirect to homepage or user dashboard
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})


# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("landing_page")  # Redirect to homepage or another page
