from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from accounts.models import GuestEmail


# When a user is created we need to create a billing profile
# Use Django signals
User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):

    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get("guest_email_id")
        created = False
        obj = None

        user = request.user
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email)

        else:
            pass

        return obj, created

# abc@chainreaders.com -> Can have a 1000 billing profiles
# But a registered user on our website user@chainreaders.com - should have
# only 1 billing profile


# Create your models here.
class BillingProfile(models.Model):
    # We want a billing profile for a guest user.
    # Therefore, null = True
    # 1 user has only 1 billing profile
    # unique = True || use OneToOne field
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    # When the guest user becomes authenticated, the multiple
    # old emails of a guest user shouldn't be active.
    # They should be based off 1 user
    email = models.EmailField()
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    # Customer ID in Stripe or Braintree

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


# If customer_ID is present for a payments app
# def billing_profile_create_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print("ACTUAL API Request -> Send to Stripe or Braintree")
#         instance.customer_id = new_id
#         instance.save()


def user_created_receiver(sender, instance, created, *args, **kwargs):
    # Whenever a user is created a billing profile is created through this signal
    if created and instance.email:
        # Create a Billing Profile object if email is present for an authenticated user
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)