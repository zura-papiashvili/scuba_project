from django.urls import path
from .views import course_list, course_detail, enroll, my_courses

urlpatterns = [
    path("", course_list, name="course_list"),
    path("<int:course_id>/", course_detail, name="course_detail"),
    path("<int:course_id>/enroll/", enroll, name="enroll"),
    path("my-courses/", my_courses, name="my_courses"),
]
