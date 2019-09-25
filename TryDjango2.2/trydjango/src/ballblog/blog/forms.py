from django import forms
from .models import BlogPost


class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)


class BlogPostModelForm(forms.ModelForm):
    # Note: The "title" field in the BlogPost model can be overridden here
    # title = forms.CharField() or title.Textarea()
    class Meta:
        model = BlogPost
        fields = ["title", "slug", "content"]

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        print(instance)
        title = self.cleaned_data.get('title')
        qs = BlogPost.objects.filter(title__iexact=title)
        # We are removing this instance from our queryset
        # We do not want to do this validation on the instance that we chnaging
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("Title already exists")
        return title
