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

    def charge(self, order_obj, card=None):
        return Charge.objects.do(self, order_obj, card)

    def get_cards(self):
        return self.card_set.all()

    @property
    def has_card(self): # Just call instance.has_card
        # Reverse relationship
        # Everything that is related to the billing profile
        card_qs = self.get_cards()
        return card_qs.exists() # Either true or false

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(default=True)
        if default_cards.exists():
            default_cards.first()

        return None

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()



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


class CardManager(models.Manager):
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, token):
        if token:
            # We know that this is a card
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card_response = customer.sources.create(source=token)
            new_card = self.model(
                billing_profile=billing_profile,
                stripe_id=card_response.id,
                brand=card_response.brand,
                country=card_response.country,
                exp_month=card_response.exp_month,
                exp_year=card_response.exp_year,
                last4=card_response.last4
            )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    stripe_id = models.CharField(max_length=120)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    brand = models.CharField(max_length=120, null=True, blank=True)
    # 2 digit code
    country = models.CharField(max_length=20, null=True, blank=True)
    exp_month = models.IntegerField(null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)


class ChargeManager(models.Manager):

    def do(self, billing_profile, order_obj, card=None):
        # Set a default card object
        card_obj = card
        if card_obj is None:
            print("Yes the card_obj is None")
            # Reverse relationship
            # Card model has BillingProfile as foreign key
            # Therefore, we can get all teh cards associated with that billing profile
            # https://stackoverflow.com/questions/42080864/set-in-django-for-a-queryset
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()

        if card_obj is None:
            print("The card object is still None")
            return False, "No cards available"

        c = stripe.Charge.create(
            amount=int(order_obj.total * 100), # Must multiply it by 100
            currency="usd",
            customer=billing_profile.customer_id,
            source=card_obj.stripe_id,
            metadata={"order_id":order_obj.order_id},
        )

        new_charge_obj = self.model(
            billing_profile=billing_profile,
            stripe_id=c.id,
            paid=c.paid,
            refunded=c.refunded,
            outcome=c.outcome,
            outcome_type=c.outcome["type"],
            seller_message=c.outcome.get("seller_message"),
            risk_level=c.outcome.get("risk_level"),
        )

        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message


class Charge(models.Model):
    stripe_id = models.CharField(max_length=120)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()
