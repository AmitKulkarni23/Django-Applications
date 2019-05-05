from django.shortcuts import render
from django.http import JsonResponse
from accounts.forms import LoginForm, GuestForm
from .models import Cart
from products.models import Product
from django.shortcuts import redirect
from orders.models import Order
from billing.models import BillingProfile
from adresses.forms import AddressForm
from adresses.models import Address
from django.conf import settings


import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_DjVHt74y3ojZJJKuXM85Q3Aq00JNC0FkIO")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", 'pk_test_y0LrxcrefvyUkATasoRO1jbZ00nhh2JLMV')

stripe.api_key = STRIPE_SECRET_KEY


def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    return cart_obj


# Create your views here.
def cart_home(request):
    context = {}
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context["cart"] = cart_obj
    return render(request, "carts/home.html", context)


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "name": x.title,
        "price": x.price,
        "url": x.get_absolute_url(),
        "id": x.id,
    }
        for x in cart_obj.products.all()]
    cart_data = {"products": products, "subtotal" : cart_obj.sub_total, "total": cart_obj.total}
    return JsonResponse(cart_data)


def cart_update(request):
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
            product_added = False
        else:
            # Add a product
            cart_obj.products.add(product_obj)  # or cart_obj.products.add(product_id)
            product_added = True
        request.session["cart_items"] = cart_obj.products.count()

        if request.is_ajax():
            # We want to send it back in JS or XML( Asynchronous Javascript nad XML)
            # In our case we will send it back in JSON format
            json_data = {
                "added": product_added,
                "removed": not product_added,
                "cartItemCount" : cart_obj.products.count(),
            }
            # Status_Code = 200 Success
            return JsonResponse(json_data, status=200)

            # Django Rest framework is better to handle all the errors
            # return JsonResponse({"message" : "Error 400"}, status=400)
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

    # Reuse addresses
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
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

        has_card = billing_profile.has_card

    if request.method == "POST":
        # Some check that order is done
        """
            Steps to finalize Checkout
            Update order_obj to be done, "paid"
            del request.session["cart_id"]
            redirect to success page 
        """
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, charge_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session["cart_items"] = 0
                del request.session["cart_id"]

                if not billing_profile.user:
                    # If billing profile doesn't have a user associated with it
                    # Set all of the cards associated with it to be inactive
                    billing_profile.set_cards_inactive()

                return redirect("carts:success")
            else:
                print(charge_msg)
                return redirect("carts:checkout")

    context = {"object": order_obj,
               "billing_profile": billing_profile,
               "login_form": login_form,
               "guest_form": guest_form,
               "address_form": shipping_address_form,
               "address_qs": address_qs,
               "has_card" : has_card,
               "publish_key": STRIPE_PUB_KEY,
               }
    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    context = {}
    return render(request, "carts/checkout-done.html", context)
