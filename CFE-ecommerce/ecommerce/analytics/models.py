from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from .signals import object_viewed_signal
from .utils import get_client_ip
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from accounts.signals import user_logged_in_signal

User = settings.AUTH_USER_MODEL

FORCE_USER_SESSION_END = getattr(settings, 'FORCE_USER_SESSION_END', False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)


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


class UserSession(models.Model):
    # Even if teh user is not logged in we want to capture info
    # The actual user instance
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    # Note: There is an IP Field in Django models
    ip_address = models.CharField(max_length=220, blank=True, null=True)

    # Session key
    session_key = models.CharField(max_length=100, null=True, blank=True)

    # We want to know when the user viewed a page, therefore we need a timestamp
    timestamp = models.DateTimeField(auto_now_add=True)

    # Whether the session is active or not
    active = models.BooleanField(default=True)

    # Whether or not we ant to manually end a session
    ended = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.ended = True
            self.active = False
            self.save()
        except:
            pass

        return self.ended


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)

        for item in qs:
            item.end_session()

    if not instance.active and not instance.ended:
        instance.end_session()


if FORCE_USER_SESSION_END:
    post_save.connect(post_save_session_receiver, sender=UserSession)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    # User is logged in
    print(instance)
    ip_address = get_client_ip(request)
    user = instance
    session_key = request.session.session_key

    # Create a new session
    UserSession.objects.create(user=user, ip_address=ip_address, session_key=session_key)


user_logged_in_signal.connect(user_logged_in_receiver)


def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        # This user was not created now
        # We went into the admin and deactivated this user
        # Need to end / delete the session related to this User
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)

        for item in qs:
            item.end_session()


if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)
