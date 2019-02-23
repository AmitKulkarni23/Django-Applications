from django.shortcuts import render, get_object_or_404
from .forms import ArticleForm
from django.urls import reverse

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

from .models import Article


class ArticleListView(ListView):
    # need to provide a queryset
    # You can override the generic one
    template_name = "articles/article_list.html"
    queryset = Article.objects.all() # WIll look for template in articles/article_list.html


class ArticleDetailView(DetailView):
    # need to provide a queryset
    # You can override the generic one
    template_name = "articles/article_detail.html"
    queryset = Article.objects.all()  # WIll look for template in articles/article_list.html

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)


class ArticleCreateView(CreateView):
    # Creating a new blog article
    # This is a form
    template_name = "articles/article_create.html"
    form_class = ArticleForm
    queryset = Article.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    # Updating an existing article
    # Since we will be updating a single article
    # call the get object method
    template_name = "articles/article_create.html"
    form_class = ArticleForm
    queryset = Article.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)


class ArticleDeleteView(DeleteView):
    # need to provide a queryset
    # You can override the generic one
    template_name = "articles/article_delete.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)

    def get_success_url(self):
        """
        Where do you point your URL to after a successful deletion
        :return: The name of teh urlpattern that will be pointed to
        """
        return reverse("articles:article-list")