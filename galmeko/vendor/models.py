from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, blank=False, null=False)
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Active'),
        (2, 'Rejected'),
        (3, 'Deleted'),
    )
    status = models.IntegerField(
        _('status'), choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendor'

    def __str__(self):
        return self.company_name


class Driver(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(_('email address'), unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
        (3, 'Deleted'),

    )
    status = models.IntegerField(
        _('type'), choices=STATUS_CHOICES, default=1)
    image = models.ImageField(null=True, blank=True, upload_to="driver/")
    address = models.CharField(max_length=150, blank=False, null=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by_id = models.IntegerField(_('deteted by'), blank=True, null=True)

    class Meta:
        db_table = "driver"

    def __str__(self):
        return self.email
