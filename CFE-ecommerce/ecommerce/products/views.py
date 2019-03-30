from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import Product
from ecommerce.utils import unique_slug_generator
from django.db.models.signals import pre_save
from carts.models import Cart


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
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
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
    # queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, object_list=None, **kwargs):
        """
        This is a method that is provided by Django.Every single class based view has this context
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get("pk")

        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Detail View is raising an error. Such a product deosn't exist")

        return instance


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

    instance = Product.objects.get_by_id(id=pk)
    # print("Instance is ", instance)
    if not instance:
        raise Http404("The get by id returned a None. Product doesn't exist")

    # # Another type of lookup
    # qs = Product.objects.filter(pk=pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("product doesn't exist")

    context = {
        "object": instance
    }

    return render(request, "products/detail.html", context)


# ===========================================================


class ProductFeaturedListView(ListView):
    template_name = "products/product_list.html"

    def get_queryset(self, *args, **kwargs):
        """
        Overriding the get_queryset method
        :param args:
        :param kwargs:
        :return:
        """
        return Product.objects.featured()


class ProductFeaturedDetailView(DetailView):
    """
    Detail View of a dfeatured object
    """
    template_name = "products/featured-detail.html"
    queryset = Product.objects.featured()

    # def get_queryset(self, *args, **kwargs):
    #     """
    #     Overriding the get_queryset method
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     return Product.objects.featured()


# ===========================================================
class ProductDetailSlugView(DetailView):
    """
    To handle URLs based on slugs
    """
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, object_list=None, **kwargs):
        """
        This is a method that is provided by Django.Every single class based view has this context
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj

        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        # instance = get_object_or_404(Product, slug=slug)
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Product Not found")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Woaaahhh!!!")
        return instance


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# This is a Signal
# Before anything goes into the db this is executed
pre_save.connect(product_pre_save_receiver, sender=Product)


