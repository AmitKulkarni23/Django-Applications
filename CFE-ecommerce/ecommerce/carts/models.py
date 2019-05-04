from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):

    def new_or_get(self, request):
        # We dont want to create a cart if it already exists
        cart_id = request.session.get("cart_id", None)

        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_obj = True
            cart_obj = self.new(user=request.user)
            request.session["cart_id"] = cart_obj.id

        return cart_obj, new_obj

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
    sub_total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


# This method will be called whenever the user hits save in teh admin panel
def m2m_changed_cart_receiver(sender, instance, action,  *args, **kwargs):
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        products = instance.products.all()
        total = 0
        for item in products:
            total += item.price

        instance.sub_total = total
        instance.save()


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.sub_total > 0:
        instance.total = float(instance.sub_total) * 1.09
    else:
        instance.total = 0.0


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)
pre_save.connect(pre_save_cart_receiver, sender=Cart)
