from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template


def home_page(request):
    my_title = "Home Page"
    return render(request, "home.html", {"title": my_title})


def about_page(request):
    my_title = "About Us"
    return render(request, "about.html", {"title": my_title})


def contact_page(request):
    my_title = "Contact Us"
    return render(request, "contact.html", {"title": my_title})


def example_page(request):
    template_name = "home.html"
    template_obj = get_template(template_name)
    context = {"title": "Example"}
    return HttpResponse(template_obj.render(context))

