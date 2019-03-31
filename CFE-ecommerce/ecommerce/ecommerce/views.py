from django.shortcuts import render
from .forms import ContactForm
from django.http import JsonResponse, HttpResponse


def home_page(request):
    # print(request.session.get("first_name", "Unknown"))
    context = {
        "title": "Hello World!"
    }
    if request.user.is_authenticated:
        context["premium_content"] = "YEAAAAHH PREMIUM USER"
    return render(request, "home_page.html", context)


def about_page(request):
    context = {"title": "About Page"}
    return render(request, "home_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Page",
        "form": contact_form,
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message" : "Thank You"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type="application/json")

    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get("full_name"))
    return render(request, "contact/view.html", context)



