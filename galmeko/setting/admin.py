from django.contrib import admin
from .forms import CustomVehicleCreationForm,CustomCategoryCreationForm
from django.utils.html import format_html
from django.urls import path
from django.conf.urls import include, url
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import ugettext_lazy
from user.admin import admin_site
from setting.models import Vehicle, VehicleCategory


class VehicleAdmin(admin.ModelAdmin):
    form = CustomVehicleCreationForm
    change_list_template = 'admin/vehicle/change_list.html'
    model = Vehicle
    list_display = ('vehicle_no', 'chassis_no', 'status', 'category_name')
    list_filter = ('status',)
    list_per_page = 5

    fieldsets = (
        (None, {'fields': ('vehicle_no', 'chassis_no', 'status')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('vehicle_no', 'chassis_no', 'status')}
         ),
    )
    search_fields = ('company_name',)
    ordering = ('-id',)

    def category_name(self, obj):
        objs = VehicleCategory.objects.filter(
            id=obj.vehicle_category_id).first()
        if objs == None:
            category = 'Not Available'
        else:
            category = objs.category_name

        return category

    def save_vehicle(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()


class VehicleCategoryAdmin(admin.ModelAdmin):
    form = CustomCategoryCreationForm
    model = VehicleCategory
    list_display = ('category_name', 'status')
    list_filter = ('category_name', 'status',)
    list_per_page = 5

    fieldsets = (
        (None, {'fields': ('category_name', 'status')}),
    )
    search_fields = ('category_name', 'status',)
    ordering = ('-id',)


admin_site.register(VehicleCategory, VehicleCategoryAdmin)
admin_site.register(Vehicle, VehicleAdmin)
