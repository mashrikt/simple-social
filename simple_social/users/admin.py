from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_email_verified', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Geolocation'), {'fields': ('registration_ip', 'location_data', 'is_date_joined_local_holiday')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_email_verified')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(EmailAddress)
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(TokenProxy)
