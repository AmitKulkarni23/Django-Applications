from django.shortcuts import render

from .models import Product
from .forms import ProductForm
from .forms import RawProductForm


# Create your views here.
def product_detail_view(request):
    obj = Product.objects.get(id=1)
    # context = {
    #     'title': obj.title,
    #     'description': obj.description
    # }
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
