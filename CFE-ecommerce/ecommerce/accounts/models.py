from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, is_active=True, is_staff=False, is_admin=False, password=None):
        """
        Creates and saves a User with the given email and password.
        Method takes in all the required fields
        email and password are required
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError("Users must have a password")

        if not full_name:
            raise ValueError("Users must have a full name")

        # Normalize our email for us
        user = self.model(
            email=self.normalize_email(email),
        )

        # Use user.set_password()
        # Not user.password = password
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.full_name = full_name
        user.set_password(password)
        user.save(using=self._db)

        # return the user instance
        return user

    def create_staffuser(self, email, full_name, password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            full_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        print("Is this the method being called")
        user = self.create_user(
            email,
            full_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name'] # Email & Password are required by default.

    # Use the model manager
    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    # These are model level permissions
    # These are required
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
