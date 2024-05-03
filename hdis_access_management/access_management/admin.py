from .models import Member
from .forms import MemberCreationForm, MemberChangeForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class MemberAdmin(UserAdmin):
    """Django Admin configuration for Member model."""

    model = Member

    # Forms used to add and update new Member instances
    add_form = MemberCreationForm
    form = MemberChangeForm

    # The fields to be used in displaying the User model. These override the definitions on 
    # the base UserAdmin class that reference specific fields on auth.User.
    list_display = ('username', 'name', 'mobile', 'email', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')    #Filters will be enabled for these fields
    fieldsets = (
        (None, {'fields': ('username', 'password', 'last_login', 'date_joined')}),
        ('Personal info', {'fields': ('name', 'email', 'mobile')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    )
    
    # Dev Note: add_fieldsets is not overridden and remains set to ('username', 'password1', 'password2')
    
    # Inbuilt Search functionality will search the contents of these fields.
    search_fields = ('username', 'name', 'mobile', 'email')

    # Controls ordering of the Member list.
    ordering = ('username',)


admin.site.register(Member, MemberAdmin)