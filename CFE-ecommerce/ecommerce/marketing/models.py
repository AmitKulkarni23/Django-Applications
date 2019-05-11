from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save

from .utils import Mailchimp

# Create your models here.
class MarketingPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Whether  this user is subscribed to Mailchimp
    # This is related to our database
    # If subscribe changes then we want to delete such a user from teh mailchimp mailing list
    subscribed = models.BooleanField(default=True)
    mailchimp_msg = models.TextField(null=True, blank=True) # will be realted to an API call
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    mailchimp_subscribed = models.NullBooleanField(blank=True)

    def __str__(self):
        return self.user.email


def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        status_code, response_data = Mailchimp().resubscribe(instance.user.email)
        print("Status Code = ", status_code)
        print("Response Data = ", response_data)


post_save.connect(marketing_pref_create_receiver, sender=MarketingPreference)


# We want to create this Marketing model whenever the user is created
def make_make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
    """
    User model
    """
    if created:
        MarketingPreference.objects.get_or_create(user=instance)


post_save.connect(make_make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)


def marketing_pref_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            status_code, response_data = Mailchimp().resubscribe(instance.user.email)
        else:
            status_code, response_data = Mailchimp().unsubscribe(instance.user.email)

        if response_data["status"] == "subscribed":
            instance.mailchimp_subscribed = True
            instance.subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.mailchimp_subscribed = False
            instance.subscribed = False
            instance.mailchimp_msg = response_data


pre_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)
