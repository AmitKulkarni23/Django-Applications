from django.urls import path
from .views import (
    CourseView,
    CourseListView,
    CourseCreateView,
)

app_name = "courses"
urlpatterns = [
    path("<int:id>", CourseView.as_view(), name="courses-detail"),
    path("", CourseListView.as_view(), name="courses-list"),
    path("create/", CourseCreateView.as_view(), name="courses-create"),
]