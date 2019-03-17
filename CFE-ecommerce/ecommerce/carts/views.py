from django.shortcuts import render
from .models import Cart
from products.models import Product
from django.shortcuts import redirect


def cart_create(user=None):
    print("New cart created")
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

    return redirect("carts:home")

