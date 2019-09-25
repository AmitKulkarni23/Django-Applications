from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from .forms import ContactForm


def home_page(request):
    my_title = "Home Page"
    return render(request, "home.html", {"title": my_title})


def about_page(request):
    my_title = "About Us"
    return render(request, "about.html", {"title": my_title})


def contact_page(request):
    my_title = "Contact Us"
    form = ContactForm(request.POST or None)

    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()

    context = {
        "title" : my_title,
        "form" : form,
    }
    return render(request, "form.html", context)


def example_page(request):
    template_name = "home.html"
    template_obj = get_template(template_name)
    context = {"title": "Example"}
    return HttpResponse(template_obj.render(context))

