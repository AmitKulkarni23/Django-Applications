import decimal

from django.db import models
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
import math
from billing.models import BillingProfile


# (db _stored_value, display_value)
ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"),
)


# Create your models here.
class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    # shipping_address = ?
    # billing_address = ?

    # Assign a random of strings / numbers which represents this order to the customer
    # pk / id
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default="created", choices=ORDER_STATUS_CHOICES)

    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    # helper function
    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = format(math.fsum([cart_total, shipping_total]), ".2f")

        self.total = new_total
        self.save()

        return new_total


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        # Just to avoid confusion
        cart_obj = instance

        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)

        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)

# Generate the order_id
# Generate the order total