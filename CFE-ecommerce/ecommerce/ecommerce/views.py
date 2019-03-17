from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model


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

    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get("full_name"))
    return render(request, "contact/view.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    # This is built into Django
    # print("User logged in")
    # print(request.user.is_authenticated)
    if form.is_valid():
        user = authenticate(request,
                            username=form.cleaned_data.get("user_name"),
                            password=form.cleaned_data.get("password"))
        if user is not None:
            # Login the user
            login(request, user)

            # Create a new instance of the form
            # That is clearing the form
            context["form"] = LoginForm()

            # Redirect to teh login page again( success page )
            return redirect("/login")
        else:
            print("Error")
    return render(request, "auth/login.html", context)


# Use the user model
User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form" : form
    }

    if form.is_valid():
        print(form.cleaned_data)
        user_name = form.cleaned_data.get("user_name")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username=user_name, password=password, email=email)
        print(new_user)
    return render(request, "auth/register.html", context)

