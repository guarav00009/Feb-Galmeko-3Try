from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Value
from django.db.models.functions import Concat
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50,blank=False,null=False) 
    last_name = models.CharField(max_length=50,blank=False,null=False)
    STATUS_CHOICES = (
        (1, 'Hospital'),
        (2, 'Vendor'),
        (3, 'User'),
        (4, 'Admin'),

    )
    type = models.IntegerField(
        _('type'), choices=STATUS_CHOICES, default=4)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    deleted_at = models.DateField(_('deteted at'), blank=True, null=True)
    deleted_by_id = models.IntegerField(_('deteted by'), blank=True, null=True)

    def __str__(self):
        return self.email

    def get_name(self):
        return self.first_name.capitalize() + ' ' + self.last_name.capitalize()

    class Meta:
        verbose_name_plural = 'Users'

    get_name.allow_tags = True
    get_name.short_description = 'name'
    get_name.admin_order_field = Concat('first_name', Value(' '), 'last_name')


class EmailTemplate(models.Model):
    type = models.CharField(max_length=150)
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
        (2, 'Deleted'),
    )
    template = models.TextField(blank=True, null=True)
    is_active = models.IntegerField(
        _('status'), choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.type