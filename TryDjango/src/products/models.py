from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.TextField(default='Basketball')
    description = models.TextField(default='This is my 1st model')
    price = models.TextField(default='100')
    summary = models.TextField(default='This is cool')
