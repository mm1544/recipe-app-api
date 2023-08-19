"""
Django admin customization.
"""
from django.contrib import admin
# We importing UserAdmin and will be making changes to it.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Integrates with the Django translation system. So if you will \
# change language of Dj (and you want to change it everywhere \
# in the project), then you can do it in the configuration. \
# Using '_' will translate the text.
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    # !!!!
    # Need to make customization to UserAdmin so that it supports \
    # all of the fields on our custom user model instead of the \
    # fields defined in BaseUserAdmin class
    fieldsets = (
        # 'None' -> Title section is missing
        (None, {'fields': ('email', 'password')}),
        # Importing the translation (???)
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    # Will make 'last_login' field readonly
    readonly_fields = ['last_login']

    add_fieldsets = (
        (None, {
            # For better visual look
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


# If you not specify UserAdmin, then Dj will use a \
# default model manager with simple CRUD operations, \
# and it would not apply the changes that we have applied \
# in our custom UserAdmin class.
admin.site.register(models.User, UserAdmin)
