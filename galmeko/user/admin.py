
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from hospital.forms import CustomHospitalCreationForm
from vendor.forms import CustomVendorCreationForm
from setting.forms import CustomVehicleCreationForm
from django.contrib.auth.models import Group
from .models import User,EmailTemplate
from hospital.models import Hospital
from vendor.models import Vendor
from setting.models import Vehicle
from django.urls import path
from django.conf.urls import include, url
from django.template.response import TemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import ugettext_lazy
from django.shortcuts import redirect, render
from .admin_view import get_vehicle_list, delete_vehicle, get_driver_list
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django import forms
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin
import binascii,os
from django.template import Context, Template 
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class MyAdminSite(admin.AdminSite):
    index_title = ugettext_lazy('Admin')

    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the admin site.

        For sites running on a subpath, use the SCRIPT_NAME value if site_url
        hasn't been customized.
        """
        self.site_title = ugettext_lazy('User')
        self.index_title = ugettext_lazy('Dashboard')
        self.site_header = ugettext_lazy('GLEMKO')

        script_name = request.META['SCRIPT_NAME']
        site_url = script_name if self.site_url == '/' and script_name else self.site_url
        return {
            'site_title': self.site_title,
            'site_header': self.site_header,
            'site_url': site_url,
            'has_permission': self.has_permission(request),
            'available_apps': self.get_app_list(request),
            'is_popup': False,
        }

    def get_urls(self):
        urls = super(MyAdminSite, self).get_urls()
        my_urls = [
            url('^get-vehicle/', self.admin_view(get_vehicle_list)),
            url('^delete_vehicle/', self.admin_view(delete_vehicle)),
            url('^get-driver/', self.admin_view(get_driver_list)),
        ]
        return my_urls + urls


admin_site = MyAdminSite()


class HospitalInline(admin.TabularInline):
    model = Hospital
    form = CustomHospitalCreationForm


class VendorInline(admin.TabularInline):
    model = Vendor
    form = CustomVendorCreationForm


class VehicleInline(admin.TabularInline):
    extra = 1
    model = Vehicle
    form = CustomVehicleCreationForm


class UserAdmin(UserAdmin):
    inlines = [
        HospitalInline, VendorInline, VehicleInline
    ]
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ('first_name', 'last_name', 'user_type',
                    'email', 'is_staff', 'is_active',)
    list_filter = ('is_active',)
    list_per_page = 10  # No of records per page
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password', 'type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'is_staff', 'is_active', 'type')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def user_type(self, obj):
        get_type = User.objects.get(id=obj.id)
        user_type = get_type.type
        if user_type == 1:
            type = 'Hospital'
        elif user_type == 2:
            type = 'Vendor'
        elif user_type == 4:
            type = 'Admin'
        else:
            type = 'User'

        return type
        user_type.short_description = "Type"
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change and form.cleaned_data['password1']:
            key =  binascii.hexlify(os.urandom(20)).decode()
            token_data = Token.objects.create(key=key,user_id=obj.id)
            save_token = token_data.save()
        if save_token is None:
            sendTo = form.cleaned_data['email']
            name = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
            password = form.cleaned_data['password1']
            msg_plain = 'Login Details ' +  name + ' / ' + password
            getTemplate = EmailTemplate.objects.get(pk=1)
            templates = Template(getTemplate.template)
            tokendata = Token.objects.get(user_id = obj.id)
            context = Context(
                {
                    'name': name,
                    'password' : password,
                    'base_url' : settings.SITE_BASE_URL,
                    'uid'      : urlsafe_base64_encode(force_bytes(obj.id)),
                    'token'    : tokendata.key
                }
             )
            print(context)
            msg_html = templates.render(context)
            send_mail(
                'Registration Successfully.',
                msg_plain,
                settings.FROM_EMAIL,
                [sendTo],
                fail_silently=False,
                html_message=msg_html,
            )


admin_site.register(User, UserAdmin)
