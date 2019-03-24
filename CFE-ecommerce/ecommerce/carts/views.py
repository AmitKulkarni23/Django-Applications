from django.shortcuts import render

from accounts.forms import LoginForm, GuestForm
from .models import Cart
from products.models import Product
from django.shortcuts import redirect
from orders.models import Order
from billing.models import BillingProfile
from adresses.forms import AddressForm
from adresses.models import Address


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

    login_form = LoginForm()
    guest_form = GuestForm()
    shipping_address_form = AddressForm()

    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        order_obj, order_ob_created = Order.objects.new_or_get(billing_profile, cart_obj)

        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)

            # Delete the session variable now
            del request.session["shipping_address_id"]

        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            # Delete the session variable now
            del request.session["billing_address_id"]

        if billing_address_id or shipping_address_id:
            # If we either have a shipping address or a billing address save the order
            order_obj.save()

    context = {"object": order_obj,
               "billing_profile": billing_profile,
               "login_form": login_form,
               "guest_form": guest_form,
               "address_form": shipping_address_form,
               }
    return render(request, "carts/checkout.html", context)

