from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class BlogPost(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        return f"/blog/{self.slug}/edit"

    def get_delete_url(self):
        return f"/blog/{self.slug}/delete"

