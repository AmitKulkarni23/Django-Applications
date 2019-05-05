from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


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

    def __str__(self):
        return self.user.email


def marketing_pref_update_receiver(sender, instance, created, *args, **kwargs):
    if created:
        pass
        print("Add user to mailchimp")


post_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)


# We want to create this Marketing model whenever the user is created
def make_make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
    """
    User model
    """
    if created:
        MarketingPreference.objects.get_or_create(user=instance)


post_save.connect(make_make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)