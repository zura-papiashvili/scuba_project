from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required


# Create your views here.
def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {"courses": courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "courses/course_detail.html", {"course": course})


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    enrollment = Enrollment.objects.create(course=course, user=user)
    return HttpResponse("You are enrolled!")


@login_required
def my_courses(request):
    user = request.user
    enrollments = Enrollment.objects.filter(user=user)
    return render(request, "courses/my_courses.html", {"enrollments": enrollments})
