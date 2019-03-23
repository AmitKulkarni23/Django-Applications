from django.shortcuts import render

from accounts.forms import LoginForm, GuestForm
from .models import Cart
from products.models import Product
from django.shortcuts import redirect
from orders.models import Order
from billing.models import BillingProfile
from accounts.models import GuestEmail


def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    return cart_obj


# Create your views here.
def cart_home(request):
    context = {}
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context["cart"] = cart_obj
    return render(request, "carts/home.html", context)


def cart_update(request):
    print(request.POST)
    product_id = request.POST.get("product_id")
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user. Product is gone")
            return redirect("carts:home")

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            # Remove a product
            cart_obj.products.remove(product_obj)
        else:
            # Add a product
            cart_obj.products.add(product_obj)  # or cart_obj.products.add(product_id)
        request.session["cart_items"] = cart_obj.products.count()
    return redirect("carts:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None

    if cart_created or cart_obj.products.count() == 0:
        # Means that the cart is created in this view
        # Cart initially did not exist
        # We want cart to handle this
        # We also want to ensure that there are no products in the cart
        return redirect("carts:home")

    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()

    guest_email_id = request.session.get("guest_email_id")

    user = request.user
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)

    else:
        pass

    if billing_profile is not None:
        # If there is any order on this cart and is active, we will make such an order being inactive now
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            # Doesn't exist
            # Create the order

            # Get rid of old ones
            # Get everything except teh one with this billing profile
            old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)

            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

    context = {"object": order_obj,
               "billing_profile": billing_profile,
               "login_form": login_form,
               "guest_form": guest_form
               }
    return render(request, "carts/checkout.html", context)

