from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, GuestForm
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url
from .models import GuestEmail

# Create your views here.


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email)
        request.session["guest_email_id"] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/")

    return redirect("/register/")


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    # This is built into Django
    # print("User logged in")
    # print(request.user.is_authenticated)
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        user = authenticate(request,
                            username=form.cleaned_data.get("user_name"),
                            password=form.cleaned_data.get("password"))
        if user is not None:
            # Login the user
            login(request, user)

            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")

            # Create a new instance of the form
            # That is clearing the form
            context["form"] = LoginForm()

            # Redirect to teh login page again( success page )
            return redirect("/login")
        else:
            print("Error")
    return render(request, "accounts/login.html", context)


# Use the user model
User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form" : form
    }

    if form.is_valid():
        user_name = form.cleaned_data.get("user_name")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username=user_name, password=password, email=email)
    return render(request, "accounts/register.html", context)
