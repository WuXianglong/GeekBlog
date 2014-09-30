# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

from geekblog.admin.filters import ActionFlagFilter
from geekblog.admin.sites import custom_site
from geekblog.usermanagement.models import CustomGroup, CustomUser
from geekblog.usermanagement.forms import CustomUserCreationForm, CustomUserChangeForm

_LOG_ACTIONS = {
    ADDITION: _('addition action'),
    CHANGE: _('change action'),
    DELETION: _('deletion action'),
}


class CustomAuthAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        self.has_change = False
        super(CustomAuthAdmin, self).__init__(model, admin_site)

    def get_model_perms(self, request):
        perms = super(CustomAuthAdmin, self).get_model_perms(request)
        perms.update({'view': self.has_view_permission(request)})
        return perms

    def changelist_view(self, request, extra_context=None):
        if self.has_view_permission(request, None):
            self.has_change = True
        if not extra_context:
            extra_context = {}
        extra_context.update({'has_change_permission': request.user.has_perm(self.opts.app_label +
                              '.' + self.opts.get_change_permission())})
        result = super(CustomAuthAdmin, self).changelist_view(request, extra_context=extra_context)
        self.has_change = False
        return result

    def has_view_permission(self, request, obj=None):
        opts = self.opts
        view_permission = 'view_%s' % self.model._meta.model_name
        return request.user.has_perm(opts.app_label + '.' + view_permission)

    def has_change_permission(self, request, obj=None):
        if getattr(self, 'has_change', False):
            return True
        return super(CustomAuthAdmin, self).has_change_permission(request, obj)

    def change_view(self, request, object_id, extra_context=None):
        if self.has_view_permission(request, None):
            self.has_change = True
        result = super(CustomAuthAdmin, self).change_view(request, object_id, extra_context=extra_context)
        self.has_change = False
        return result

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        old_has_change = self.has_change
        self.has_change = False
        context.update({'has_sync_to_permission': False})
        result = super(CustomAuthAdmin, self).render_change_form(request, context, add=add, change=change, form_url=form_url, obj=obj)
        if old_has_change:
            self.has_change = True
        return result


class LogEntryAdmin(CustomAuthAdmin):
    list_display = ('user', 'content_type', 'object_repr', 'action_time', 'display_action_flag')
    list_filter = ('user', ActionFlagFilter)
    readonly_fields = ('user', 'content_type', 'object_id', 'object_repr', 'action_time', 'action_flag', 'change_message')
    list_per_page = 50
    search_fields = ['user__username', 'content_type__name']

    def has_add_permission(self, request, obj=None):
        return False

    def display_action_flag(self, obj):
        return _LOG_ACTIONS[obj.action_flag]
    display_action_flag.short_description = _('action flag')


class CustomUserAdmin(UserAdmin, CustomAuthAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'activation_code')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'qq', 'website')}),
        (_('Permissions'), {'fields': ('status', 'is_staff', 'is_active', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_filter = ('is_staff', 'is_superuser', 'status', 'groups')
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm


class CustomGroupAdmin(GroupAdmin, CustomAuthAdmin):
    pass

custom_site.register(LogEntry, LogEntryAdmin)
custom_site.register(CustomGroup, CustomGroupAdmin)
custom_site.register(CustomUser, CustomUserAdmin)
