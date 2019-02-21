from django.shortcuts import render

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


