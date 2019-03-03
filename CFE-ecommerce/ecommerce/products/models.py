from django.db import models
import random
import os


def get_filename_extension(filepath):
    """
    Helper function to extract the extension of the filename
    :param filename: Name of the file
    :return: the extension of the file
    """
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)

    return name, ext


def upload_image_path(instance, filename):
    """
    Helper function to change the filename of the uploaded file
    Needed because the file being uploaded might have spaces in it
    :param instance:
    :param filename:
    :return: Chnage the uploaded filename to a random integer
    """
    print(instance)
    print(filename)
    new_file_name = random.randint(1, 31920002)
    name, ext = get_filename_extension(filename)
    final_filename = "{new_file_name}{ext}".format(new_file_name=new_file_name, ext=ext)
    return f"products/{new_file_name}/{final_filename}"


class ProductManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def featured(self):
        return self.filter(featured=True)


# Create your models here.
class Product(models.Model):
    """
    The model for a product
    """
    title = models.CharField(max_length=120)

    # Adding a slug field
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=9.99)

    # It uploads to media root
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    # Featured product
    featured = models.BooleanField(default=False)

    # Extending your custom model manager
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/products/{self.slug}"


