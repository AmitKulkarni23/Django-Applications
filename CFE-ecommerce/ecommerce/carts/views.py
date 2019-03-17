from django.shortcuts import render


# Create your views here.
def cart_home(request):
    # key = request.session.session_key

    request.session["first_name"] = "Amit"
    # Expire the session key after 300 seconds
    # request.session.set_expiry(300)
    return render(request, "carts/home.html", {})
