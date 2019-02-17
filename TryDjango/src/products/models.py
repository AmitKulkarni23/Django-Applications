from django.db import models


# Create your models here.
class Product(models.Model):
    # Title field should be limited to how long it is
    title = models.CharField(max_length=120)

    description = models.TextField(blank=True, null=True)

    # Decimal Field
    price = models.DecimalField(decimal_places=2, max_digits=1000)

    # Summary is a text field
    summary = models.TextField(blank=False, null=False)

    featured = models.BooleanField(default=False)

