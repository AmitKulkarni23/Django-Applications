from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import BlogPost
from .forms import BlogPostForm, BlogPostModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


def blog_post_list_view(request):
    # Can list out objects
    # Can also be a search view
    # get all of the objects in the database
    qs = BlogPost.objects.all()

    template_name = "blog/list.html"
    context = {"object_list" : qs}
    return render(request, template_name, context)

# This is a wrapper that checks if the user is logged in or not
@login_required
def blog_post_create_view(request):
    # Create objects
    # How? - use forms
    form = BlogPostForm(request.POST or None) # This is just the form
    form = BlogPostModelForm(request.POST or None) # This is teh model form

    if form.is_valid():
        # obj = BlogPost.objects.create(**form.cleaned_data)
        # form = BlogPostForm()
        form.save()
        form = BlogPostModelForm()

    template_name = "blog/form.html"
    context = {"form": form}
    return render(request, template_name, context)


def blog_post_detail_view(request, slug):
    # 1 object
    # OR detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/detail.html"
    context = {"object": obj}
    return render(request, template_name, context)


def blog_post_update_view(request, slug):
    # Will have to grab the original object
    # Need to update that object
    template_name = "blog/update.html"
    obj = get_object_or_404(BlogPost, slug=slug)
    context = {"form": None, "object": obj}
    return render(request, template_name, context)


def blog_post_delete_view(request, slug):
    template_name = "blog/delete.html"
    obj = get_object_or_404(BlogPost, slug=slug)
    context = {"object": obj}
    return render(request, template_name, context)
