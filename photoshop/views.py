from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
import json
import requests
from .helpers import validate_parameters
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import ProcessedImage
from django_ratelimit.decorators import ratelimit


API_KEY = os.getenv("API_KEY")


def home(request):
    return render(request, "photoshop/scuba_photo.html")


@csrf_exempt
@login_required
@ratelimit(key="user", rate="1/h", block=False)
def process_image(request):

    if getattr(request, "limited", False):
        return render(request, "photoshop/rate_limit_error.html")
    # Extracting the uploaded file and parameters from the request
    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    # Validate parameters
    params = {
        "key": request.POST.get("key", "E337EC114A9F3035DEBD6AF387A3E3A7"),
        "numlevels": int(request.POST.get("numlevels", 8)),
        "omega": request.POST.get("omega", "1/r"),
        "alpha": int(request.POST.get("alpha", 5)),
        "method": request.POST.get("method", "interp"),
        "degree": int(request.POST.get("degree", 9)),
        "gaussianstd": int(request.POST.get("gaussianstd", 50)),
    }

    # You must implement this validate_parameters function to handle the logic for checking if the parameters are valid
    params = validate_parameters(params)

    form_data = {
        "key": params["key"],
        "params": json.dumps(
            {
                "numlevels": params["numlevels"],
                "omega": params["omega"],
                "alpha": str(params["alpha"]),
                "method": params["method"],
                "degree": params["degree"],
                "orig_input_0": "input_0.png",
                "input_0": "input_0.png",
                "gaussianstd": params["gaussianstd"],
            }
        ),
        "clientData": json.dumps(
            {
                "demo_id": 88,
                "params": {
                    "alpha": str(params["alpha"]),
                    "omega": params["omega"],
                    "gaussianstd": params["gaussianstd"],
                    "method": params["method"],
                    "numlevels": params["numlevels"],
                    "degree": params["degree"],
                },
                "origin": "upload",
            }
        ),
    }

    # Attach the file separately
    files = {"file_0": uploaded_file}

    # API endpoint URL
    url = "https://ipolcore.ipol.im/api/core/run"

    # Send the POST request with the file and form data
    response = requests.post(url, files=files, data=form_data)

    if response.status_code == 200 or response.status_code == 201:
        # Response is successful, process the result
        response_data = response.json()

        # Extract information from the response
        status = response_data.get("status")
        work_url = response_data.get("work_url")

        # Formulate the URLs for the processed images
        image_urls = [
            f"https://ipolcore.ipol.im{work_url}/input_0.png",
            f"https://ipolcore.ipol.im{work_url}/ace.png",
            f"https://ipolcore.ipol.im{work_url}/he.png",
        ]
        # Create and save the processed image entry
        user = request.user
        processed_image = ProcessedImage.objects.create(
            user=user,
            work_url=work_url,
            photo_name="default_image.jpg",
        )

        # Return the URLs to the frontend
        return render(
            request,
            "photoshop/scuba_photo.html",
            {"status": status, "image_urls": image_urls},
        )
    else:
        # If something went wrong, return a JSON error response
        return JsonResponse({"error": response.text}, status=response.status_code)


@csrf_exempt  # Disable CSRF for testing (use authentication in production)
@require_POST
@login_required
def create_processed_image(request):
    try:
        # Parse JSON data from the body
        data = json.loads(request.body)

        # Extract fields from the JSON data

        user = request.user
        work_url = data.get("work_url", "https://example.com")
        photo_name = data.get("photo_name", "default_image.jpg")

        # Create and save the processed image entry
        processed_image = ProcessedImage.objects.create(
            user=user,
            work_url=work_url,
            photo_name=photo_name,
        )

        return JsonResponse(
            {"message": "Processed image saved successfully", "id": processed_image.id},
            status=201,
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


@login_required
def user_processed_images(request):

    # Get the current user
    user = request.user

    # Retrieve all processed images for the user
    processed_images = ProcessedImage.objects.filter(user=user)
    print("test")
    # Render the template with the processed images
    return render(
        request,
        "photoshop/user_processed_images.html",
        {"processed_images": processed_images},
    )
