from django.shortcuts import render
from django.views.generic import ListView, DetailView
from products.models import Product


# Create your views here.
class SearchProductView(ListView):
    template_name = "products/product_list.html"

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.featured()


