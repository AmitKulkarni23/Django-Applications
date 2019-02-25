from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    context = {"title" : "Hello World!"}
    return render(request, "home_page.html", context)


def about_page(request):
    context = {"title": "About Page"}
    return render(request, "home_page.html", context)


def contact_page(request):
    context = {"title": "Contact Page"}
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get("full_name"))
    return render(request, "contact/view.html", context)

