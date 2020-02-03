from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()
from user.helper import get_email_by_id,get_name_by_id,get_phone_by_id
from .forms import CustomHospitalCreationForm
from django.utils.html import format_html
from django.urls import path
from django.conf.urls import include, url
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import ugettext_lazy
from user.admin import admin_site
from hospital.models import Hospital
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HospitalAdmin(admin.ModelAdmin):
    list_display_links = None
    change_list_template = 'admin/hospital/change_list.html'
    form = CustomHospitalCreationForm
    model = Hospital
    list_display = ('user_name','email','hospital_name','registration_no', 'address','phone','status','file_link','Action')
    list_filter = ('status',)
    list_per_page = 5  

    fieldsets = (
        (None, {'fields': ('hospital_name','registration_no', 'address','status')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('hospital_name','registration_no', 'address','status')}
        ),
    )
    search_fields = ('hospital_name',)
    ordering = ('-id',)
        
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url('^view/(?P<hospital_id>\d+)/$', self.hospital_view),
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
        edit   = '<a class="button edit-icon" title="Edit" data-id="%s" href="/admin/user/user/%s/change/"><i class="fa fa-edit" aria-hidden="true"></i></a>&nbsp;' % (obj.user_id,obj.user_id)

        return format_html(view + edit)

    def save_hospital(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    def extra_context(self, request):
        context = admin_site.each_context(request)
        context['opts'] = Hospital._meta
        context['site_title'] = ugettext_lazy('Hospital')
        return context
    
    @method_decorator(login_required())
    def hospital_view(self, request,hospital_id):
        context = self.extra_context(request)
        context['title']      = 'Hospital Details'
        context['userDetail'] = Hospital.objects.get(user_id=hospital_id)
        context['site_title'] = ugettext_lazy('Hospital')
        return TemplateResponse(request, 'admin/hospital/hospital_view.html', context=context)

admin_site.register(Hospital,HospitalAdmin)
