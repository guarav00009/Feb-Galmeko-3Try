from django.contrib import admin
from .forms import CustomVendorCreationForm,CustomDriverCreationForm
from django.utils.html import format_html
from user.helper import get_email_by_id, get_name_by_id, get_phone_by_id
from django.urls import path
from django.conf.urls import include, url
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import ugettext_lazy
from user.admin import admin_site
from vendor.models import Vendor,Driver
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect


class VendorAdmin(admin.ModelAdmin):
    list_display_links = None
    form = CustomVendorCreationForm
    model = Vendor
    list_display = ('user_name', 'email', 'company_name',
                    'phone', 'status', 'Action')
    list_filter = ('status',)
    list_per_page = 5

    fieldsets = (
        (None, {'fields': ('company_name', 'status')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('company_name', 'status')}
         ),
    )
    search_fields = ('company_name',)
    ordering = ('-id',)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url('^view/(?P<vendor_id>\d+)/$', self.vendor_view),
        ]
        return my_urls + urls

    def email(self, obj):
        get_email = get_email_by_id(obj)
        return get_email

    def user_name(self, obj):
        get_name = get_name_by_id(obj)
        return get_name

    def phone(self, obj):
        get_phone = get_phone_by_id(obj)
        return get_phone

    def Action(self, obj):
        view = '<a class="button" title="View" href="view/%s"><i class="fa fa-eye" aria-hidden="true"></i></a>&nbsp;' % (
            obj.user_id)
        edit = '<a class="button edit-icon" title="Edit" data-id="%s" href="/admin/user/user/%s/change/"><i class="fa fa-edit" aria-hidden="true"></i></a>&nbsp;' % (
            obj.user_id, obj.user_id)
        add = '<a class="button" title="Add Driver" href="/admin/vendor/driver/add/?vid=%s"><i class="fa fa-plus" aria-hidden="true"></i></a>&nbsp;'% (
            obj.id)


        return format_html(view + edit + add)

    def save_vendor(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    def extra_context(self, request):
        context = admin_site.each_context(request)
        context['opts'] = Vendor._meta
        context['site_title'] = ugettext_lazy('Vendor')
        return context

    @method_decorator(login_required())
    def vendor_view(self, request, vendor_id):
        context = self.extra_context(request)
        context['title'] = 'Vendor Details'
        context['userDetail'] = Vendor.objects.get(user_id=vendor_id)
        context['site_title'] = ugettext_lazy('Vendor')
        return TemplateResponse(request, 'admin/vendor/vendor_view.html', context=context)

class DriverAdmin(admin.ModelAdmin):
    form = CustomDriverCreationForm
    def has_module_permission(self, request):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        from django.contrib import messages
        messages.add_message(request, messages.SUCCESS, 'Driver Added Successfully.')
        return redirect('/admin/vendor/vendor')

    def save_model(self, request, obj,form, change):
        if not change:
            vendorObj = Vendor.objects.get(id=request.GET.get('vid'))
            obj.vendor = vendorObj
            obj.save()

admin_site.register(Driver, DriverAdmin)
admin_site.register(Vendor, VendorAdmin)
