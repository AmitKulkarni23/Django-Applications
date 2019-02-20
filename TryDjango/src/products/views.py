from django.shortcuts import render, get_object_or_404, redirect

from .models import Product
from .forms import ProductForm
from .forms import RawProductForm
from django.http import Http404


# Create your views here.
def product_detail_view(request, id):
    try:
        obj = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404
    context = {
        "object" : obj
    }
    return render(request, "products/product_detail.html", context)


# How to accept data from a user
# How to save data from a POST request onto a form
def product_create_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()

        # Below Statement : So that whenever user has
        # entered a valid statement gets a fresh new form
        # to enter data into
        form = ProductForm()

    context = {
        "form" : form
    }
    return render(request, "products/product_create.html", context)


def render_initial_data(request):
    initial_data = {
        'title': "Great Title",
        'description': "Initial Title",
        'price': 10.99
    }
    form = ProductForm(request.POST or None, initial=initial_data)
    context = {
        "form" : form,
    }
    return render(request, "products/product_create.html", context)


# RAW HTML DATA
# Shows how POST and GET methods work
# What a CSRF token is
# def product_create_view(request):
#     context = {}
#     if request.method == "POST":
#         my_new_title = request.POST.get("title")
#         print("My new title is ", my_new_title)
#     return render(request, "products/product_create.html", context)


# def product_create_view(request):
#     my_form = RawProductForm()
#     if request.method == "POST":
#         my_form = RawProductForm(request.POST)
#         if my_form.is_valid():
#             # Data is good
#             print(my_form.cleaned_data)
#             Product.objects.create(**my_form.cleaned_data)
#         else:
#             print(my_form.errors)
#     context = {
#         "form" : my_form
#     }
#     return render(request, "products/product_create.html", context)


def dynamic_lookup_view(request, id):
    # obj = Product.objects.get(id=id)
    # obj = get_object_or_404(Product, id=id)
    try:
        obj = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404

    context = {
        "object" : obj
    }
    return render(request, "products/product_detail.html", context)


def product_delete_view(request, id):
    obj = get_object_or_404(Product, id=id)
    # Confirming delete
    if request.method == "POST":
        obj.delete()
        return redirect("../../")
    context = {
        "object": obj
    }
    return render(request, "products/product_delete.html", context)


def product_list_view(request):
    """
    Function that will list out all the products in a database
    :param request: the Http request object
    :return:
    """
    queryset = Product.objects.all()
    context = {
        "object_list" : queryset,
    }
    return render(request, "products/product_list_view.html", context)