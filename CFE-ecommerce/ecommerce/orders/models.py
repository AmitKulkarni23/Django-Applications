import decimal

from django.db import models
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
import math
from billing.models import BillingProfile
from adresses.models import Address

# (db _stored_value, display_value)
ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"),
)


class OrderManager(models.Manager):

    def new_or_get(self, billing_profile, cart_obj):
        # If there is any order on this cart and is active, we will make such an order being inactive now
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile,
                                        cart=cart_obj,
                                        active=True,
                                        status="created")
        if qs.count() == 1:
            obj = qs.first()
        else:
            # Doesn't exist
            # Create the order

            # Get rid of old ones
            # Get everything except teh one with this billing profile
            # old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            #
            # if old_order_qs.exists():
            #     old_order_qs.update(active=False)
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created


# Create your models here.
class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True,
                                         blank=True, related_name="shipping_address")
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True,
                                        blank=True, related_name="billing_address")

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

    objects = OrderManager()

    # helper function
    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = format(math.fsum([cart_total, shipping_total]), ".2f")

        self.total = new_total
        self.save()

        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total

        if billing_profile and shipping_address and billing_address and total:
            return True

        return False

    def mark_paid(self):
        self.status = "paid"
        self.save()

        return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


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