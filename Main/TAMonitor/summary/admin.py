from django.contrib import admin
from .models import Account, Course, Student, Instructor, Admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

class UserAdmin(UserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': (
            'is_superuser',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Account)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Admin)
admin.site.register(Course)
admin.site.unregister(Group)
admin.site.site_header = "Boston College TA Application System Overview"
