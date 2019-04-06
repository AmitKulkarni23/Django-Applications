from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from accounts.models import GuestEmail
import stripe


stripe.api_key = "sk_test_DjVHt74y3ojZJJKuXM85Q3Aq00JNC0FkIO"

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

    # Customer ID in Stripe
    # This customer id will be the unique ID for thsi customer on stripe
    customer_id = models.CharField(max_length=120, null=True, blank=True)


    objects = BillingProfileManager()

    def __str__(self):
        return self.email


# If customer_ID is present for a payments app
def billing_profile_create_receiver(sender, instance, *args, **kwargs):
    # If there is no email on teh customer, we don't want to
    # create the ID on Stripe
    if not instance.customer_id and instance.email:
        print("ACTUAL API Request -> Send to Stripe")

        # Run an API request to Stripe
        customer = stripe.Customer.create(email=instance.email)
        print(customer)
        instance.customer_id = customer.id


pre_save.connect(billing_profile_create_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    # Whenever a user is created a billing profile is created through this signal
    if created and instance.email:
        # Create a Billing Profile object if email is present for an authenticated user
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)