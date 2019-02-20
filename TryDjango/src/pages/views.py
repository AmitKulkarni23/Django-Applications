from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product


# Create your views here.
def home_view(request, *args, **kwargs):
    print(request.user)
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "home.html", {})


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})


def about_view(request, id):
    obj = Product.objects.get(id=id)
    my_context = {
        "obj" : obj,
    }
    return render(request, "about.html", my_context)


def social_view(request, *args, **kwargs):
    return HttpResponse("<h1>Social Page</h1>")