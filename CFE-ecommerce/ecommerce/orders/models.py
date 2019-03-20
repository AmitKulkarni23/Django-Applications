from django.db import models
from carts.models import Cart

# (db _stored_value, display_value)
ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"),
)


# Create your models here.
class Order(models.Model):
    # billing_profile = ?
    # shipping_address = ?
    # billing_address = ?

    # Assign a random of strings / numbers which represents this order to the customer
    # pk / id
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default="created", choices=ORDER_STATUS_CHOICES)

    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    order_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return self.order_id


# Generate the order_id
# Generate the order total