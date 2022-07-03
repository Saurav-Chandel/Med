import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.timezone import now
from app import choices


# Create your models here.


class AppUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(email__iexact=username)

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a Super Admin. Not to be used by any API. Only used for django-admin command.
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active', True)

        user = self._create_user(email, password, **extra_fields)
        return user


class User(AbstractUser):
    first_last_name = models.CharField(
        max_length=200, default=None, null=True, blank=True
    )
    email=models.EmailField(unique=True,null=False)
    phone_no = models.CharField(
        max_length=20, default=None, null=True, blank=True
    )
    email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=10, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    manager = AppUserManager()

    def __str__(self):
        return self.email


class Token(models.Model):

    token = models.CharField(max_length=300)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    token_type = models.CharField(
        max_length=20, choices=choices.TOKEN_TYPE_CHOICES
    )
    created_on = models.DateTimeField(default=now, null=True, blank=True)
    expired_on = models.DateTimeField(default=now, null=True, blank=True)


class Media(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="media",
    )
    media_file = models.FileField(upload_to="media/", blank=True, null=True)
    media_file_name = models.CharField(max_length=250, blank=True, null=True)
    file_type = models.CharField(max_length=120, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id