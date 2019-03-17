from django.db import models
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


# Create your models here.
class Cart(models.Model):
    # Any user can create a cart( authenticated or non-authenticated)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # Have the ability to have a blank cart
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)