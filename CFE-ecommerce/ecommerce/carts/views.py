from django.shortcuts import render
from .models import Cart


def cart_create(user=None):
    print("New cart created")
    cart_obj = Cart.objects.create(user=None)
    return cart_obj


# Create your views here.
def cart_home(request):
    # We dont want to create a cart if it already exists
    cart_id = request.session.get("cart_id", None)

    qs = Cart.objects.filter(id=cart_id)
    if qs.count() == 1:
        print("Cart exists")
        cart_obj = qs.first()
        if request.user.is_authenticated and cart_obj.user is None:
            cart_obj.user = request.user
            cart_obj.save()
    else:
        print("Create a new cart")
        cart_obj = Cart.objects.new(user=request.user)
        request.session["cart_id"] = cart_obj.id

    # key = request.session.session_key

    # Expire the session key after 300 seconds
    # request.session.set_expiry(300)
    return render(request, "carts/home.html", {})
