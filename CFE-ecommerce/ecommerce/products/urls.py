from django.urls import path, re_path
from .views import (
    ProductListView,
    ProductDetailSlugView,
)

app_name = "products"
urlpatterns = [
    path(r"", ProductListView.as_view()),
    re_path(r"^(?P<slug>[\w-]+)/$", ProductDetailSlugView.as_view(), name="detail"),

]
