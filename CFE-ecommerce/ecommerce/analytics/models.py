from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from .signals import object_viewed_signal
from .utils import get_client_ip

User = settings.AUTH_USER_MODEL


class ObjectViewed(models.Model):
    # Even if teh user is not logged in we want to capture info
    # The actual user instance
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    # Note: There is an IP Field in Django models
    ip_address = models.CharField(max_length=220, blank=True, null=True)

    # The idea is to get all the models that are present
    # Product, Order, Cart, Address etc..
    # Any of the models mentioned above is captured by content_type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # The object id of the model captured above
    # user_id, Product_Id, Order_ID
    object_id = models.PositiveIntegerField()

    # We can call this field and get the instance of the model
    content_object = GenericForeignKey('content_type', 'object_id')

    # We want to know when the user viewd a page, therefore we need a timestamp
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed on %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ["-timestamp"] # Most recent saved shows up first
        verbose_name = "Object Viewed"
        verbose_name_plural = "Objects Viewed"


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender) # is the same thing as instance.__class__
    # print("Sender = ", sender)
    # print("Instance = ", instance)
    # print("Request = ", request)
    # print("User = ", request.user)
    new_view_obj = ObjectViewed.objects.create(
        user=request.user,
        object_id=instance.id,
        ip_address=get_client_ip(request),
        content_type=c_type
    )


object_viewed_signal.connect(object_viewed_receiver)
