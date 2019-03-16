from django.urls import path, re_path
from .views import (
    SearchProductView,
)

app_name = "products"
urlpatterns = [
    path(r"", SearchProductView.as_view(), name="query"),
]
