from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import Product


class ProductListView(ListView):
    queryset = Product.objects.all()

    def get_context_data(self, *args, object_list=None, **kwargs):
        """
        This is a method that is provided by Django.Every single class based view has this context
        :param object_list: 
        :param kwargs:
        :return:
        """
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        print(context)
        return context


# Function based view
def product_list_view(request):
    """
    The function based view
    :param request: Http request object
    :return:
    """
    queryset = Product.objects.all()
    context = {
        "object_list": queryset
    }

    return render(request, "products/product_list.html", context)


# ===========================================================


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, object_list=None, **kwargs):
        """
        This is a method that is provided by Django.Every single class based view has this context
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context


# Function based view
def product_detail_view(request, pk=None, *args, **kwargs):
    """
    The function based view
    :param pk: The primary key for the product
    :param request: Http request object
    :return:
    """
    # instance = Product.objects.get(pk=pk)
    # Using in-built get_object_or_404 error
    # instance = get_object_or_404(Product, pk=pk)

    # # Our own version of 404
    # try:
    #     instance = Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     raise Http404("Woaahhh!!! Pump the brakes. This product doesn't exist")
    # except:
    #     print("Not sure")

    # Another type of lookup
    qs = Product.objects.filter(pk=pk)
    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("product doesn't exist")

    context = {
        "object": instance
    }

    return render(request, "products/detail.html", context)