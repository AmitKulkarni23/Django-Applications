from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    my_title = "Home Page"
    return render(request, "hello_world.html", {"title": my_title})


def about_page(request):
    my_title = "About Us"
    return render(request, "about.html", {"title": my_title})


def contact_page(request):
    my_title = "Contact Us"
    return render(request, "contact.html", {"title": my_title})

