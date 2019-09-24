from django.shortcuts import render
from django.shortcuts import Http404, get_object_or_404
# Create your views here.
from .models import BlogPost


def blog_post_list_view(request):
    # Can list out objects
    # Can also be a search view
    # get all of the objects in the database
    qs = BlogPost.objects.all()

    template_name = "blog_post_list.html"
    context = {"object_list" : qs}
    return render(request, template_name, context)


def blog_post_create_view(request):
    # Create objects
    # How? - use forms
    template_name = "blog_post_create.html"
    context = {"form": None}
    return render(request, template_name, context)


def blog_post_detail_view(request, slug):
    # 1 object
    # OR detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog_post_detail.html"
    context = {"object": obj}
    return render(request, template_name, context)


def blog_post_update_view(request, slug):
    # Will have to grab the original object
    # Need to update that object
    template_name = "blog_post_update.html"
    obj = get_object_or_404(BlogPost, slug=slug)
    context = {"form": None, "object": obj}
    return render(request, template_name, context)


def blog_post_delete_view(request, slug):
    template_name = "blog_post_delete.html"
    obj = get_object_or_404(BlogPost, slug=slug)
    context = {"object": obj}
    return render(request, template_name, context)
