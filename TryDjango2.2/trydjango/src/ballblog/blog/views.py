from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm, BlogPostModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


def blog_post_list_view(request):
    # Can list out objects
    # Can also be a search view
    # get all of the objects in the database
    qs = BlogPost.objects.all().published()
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    template_name = "blog/list.html"
    context = {"object_list": qs}
    return render(request, template_name, context)

# This is a wrapper that checks if the user is logged in or not
@login_required
def blog_post_create_view(request):
    # Create objects
    # How? - use forms
    # form = BlogPostForm(request.POST or None) # This is just the form
    form = BlogPostModelForm(request.POST or None, request.FILES or None) # This is the model form

    if form.is_valid():
        # obj = BlogPost.objects.create(**form.cleaned_data)
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
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


@staff_member_required
def blog_post_update_view(request, slug):
    # Will have to grab the original object
    # Need to update that object
    template_name = "form.html"
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {"form": form, "title": f"Update {obj.title}"}
    return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
    template_name = "blog/delete.html"
    obj = get_object_or_404(BlogPost, slug=slug)
    if request.method == "POST":
        obj.delete()
        # BUT, we want to redirect them to another view
        return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)
