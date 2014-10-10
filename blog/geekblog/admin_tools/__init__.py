# -*- coding: utf-8 -*-
import datetime
from django.db.models import F
from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.options import csrf_protect_m, get_ul_class
from django.contrib.admin.widgets import AdminRadioSelect
from django.contrib.admin.util import model_ngettext
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect

from geekblog.admin_tools.widgets import CustomForeignKeyRawIdWidget
from geekblog.geekblog.constants import SYNC_STATUS
from geekblog.datasync.sync_model import sync_obj
from geekblog.datasync.modeladapter import get_adapter
from geekblog.datasync import sync_to_production, sync_from_production


class BaseModelAdmin(admin.ModelAdmin):
    special_exclude = ('creator', 'created_time', 'modifier', 'modified_time', 'sync_status')
    special_readonly = ('creator', 'created_time', 'modifier', 'modified_time', 'sync_status')
    actions = ['delete_selected_items', 'sync_selected_items']

    def __init__(self, model, admin_site):
        self.in_add_view = False
        self.has_change = False
        self.special_fieldset = ((
            _('ReadOnly'),
            {'fields': self.special_readonly + self.readonly_fields}
        ),)
        super(BaseModelAdmin, self).__init__(model, admin_site)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        db = kwargs.get('using')
        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = CustomForeignKeyRawIdWidget(db_field.rel, self.admin_site, using=db)
        elif db_field.name in self.radio_fields:
            kwargs['widget'] = AdminRadioSelect(attrs={
                'class': get_ul_class(self.radio_fields[db_field.name]),
            })
            kwargs['empty_label'] = db_field.blank and _('None') or None

        return db_field.formfield(**kwargs)

    def get_urls(self):
        urlpatterns = super(BaseModelAdmin, self).get_urls()
        from django.conf.urls import url
        info = self.model._meta.app_label, self.model._meta.model_name
        urlpatterns += (
            url(r'^syncto$', self.sync_to_production_view, name='%s_%s_sync_to_production' % info),
            url(r'^syncfrom$', self.sync_from_production_view, name='%s_%s_sync_from_production' % info),
        )
        return urlpatterns

    def get_actions(self, request):
        actions = super(BaseModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if not self.has_sync_to_permission(request) and 'sync_selected_items' in actions:
            del actions['sync_selected_items']
        return actions

    def _sync_deleted_items(self, deleted_items):
        adapter = get_adapter(self.model)
        db_conn = adapter.conn_ops['db'](settings.MONGODB_CONF)
        update_table = adapter.conn_ops['table']
        for obj in deleted_items:
            to_obj = adapter.convert_to(obj)
            cond = {'pk': to_obj['pk']} if 'pk' in to_obj else {'id': to_obj['id']}
            db_conn.delete_item(update_table, cond)

    def delete_selected_items(self, request, queryset):
        n = queryset.count()
        deleted_items = list(queryset)
        if n:
            for obj in queryset:
                self.log_deletion(request, obj, force_unicode(obj))
            queryset.update(hided=1)
            self._sync_deleted_items(deleted_items)
            self.message_user(request, _('Successfully deleted %(count)d %(items)s.') % {
                'count': n, 'items': model_ngettext(self.opts, n)
            })
    delete_selected_items.short_description = _('Delete selected %(verbose_name_plural)s')

    def sync_selected_items(self, request, queryset):
        n = queryset.count()
        if n:
            for obj in queryset:
                sync_obj(obj, self.model)
            self.message_user(request, _('Successfully synced %(count)d %(items)s.') % {
                'count': n, 'items': model_ngettext(self.opts, n)
            })
    sync_selected_items.short_description = _('Sync selected %(verbose_name_plural)s')

    def delete_model(self, request, obj):
        result = super(BaseModelAdmin, self).delete_model(request, obj)
        self._sync_deleted_items([obj])
        return result

    @csrf_protect_m
    def sync_to_production_view(self, request):
        sync_to_production(self, request)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def has_sync_to_permission(self, request, obj=None):
        opts = self.opts
        return (opts.app_label + '.' + self._get_sync_to_permission()) in request.user.get_all_permissions()

    def _get_sync_to_permission(self):
        return 'sync_to_%s' % self.opts.object_name.lower()

    @csrf_protect_m
    def sync_from_production_view(self, request):
        sync_from_production(self, request)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def has_sync_from_permission(self, request, obj=None):
        opts = self.opts
        return (opts.app_label + '.' + self._get_sync_from_permission()) in request.user.get_all_permissions()

    def _get_sync_from_permission(self):
        return 'sync_from_%s' % self.opts.object_name.lower()

    def get_model_perms(self, request):
        perms = super(BaseModelAdmin, self).get_model_perms(request)
        perms.update({'view': self.has_view_permission(request)})
        perms.update({'syncto': self.has_sync_to_permission(request)})
        perms.update({'syncfrom': self.has_sync_from_permission(request)})
        return perms

    def _can_published_or_not(self, obj):
        """ Override in sub class if check condition is different. """
        return True, ''

    def _get_next_order(self, request):
        items = self.queryset(request).order_by('-order')
        next_order = 1 if not items else items[0].order + 1
        return next_order

    def queryset(self, request):
        return super(BaseModelAdmin, self).queryset(request).filter(hided=False)

    # you can override this method in sub class if you need.
    def _get_need_adjust_items(self, request, old_obj, new_obj):
        order_is_existed = self.queryset(request).filter(order__exact=new_obj.order)
        # if new order is not existed before, return
        if not order_is_existed:
            [], 0
        # if the model is new, set old_order using _get_next_order
        if old_obj:
            old_order, new_order = old_obj.order, new_obj.order
        else:
            old_order, new_order = self._get_next_order(request), new_obj.order
        if new_order > old_order:    # order reduce
            need_adjust_items = self.queryset(request).filter(order__gt=old_order, order__lte=new_order)
            adjust_amount = -1
        else:    # order rise
            need_adjust_items = self.queryset(request).filter(order__gte=new_order, order__lt=old_order)
            adjust_amount = 1
        return need_adjust_items, adjust_amount

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
            obj.created_time = datetime.datetime.now()
            if hasattr(obj, 'order'):
                obj.order = self._get_next_order(request)
        obj.modified_time = datetime.datetime.now()
        obj.modifier = request.user
        obj.sync_status = 0
        # check the published fields
        old_obj = self.model.objects.get(pk=obj.id) if obj.pk else None

        if (not old_obj or not old_obj.published) and obj.published:
            status, msg = self._can_published_or_not(obj)
            if not status:
                obj.published = False
                messages.error(request, msg)
        # when model has order field, if the model is created or order is
        # changed, adjust the model order
        if 'order' in form.clean() and (not old_obj or old_obj.order != obj.order):
            need_adjust_items, adjust_amount = self._get_need_adjust_items(request, old_obj, obj)
            # adjust order and save items
            need_adjust_items.update(order=F('order') + adjust_amount, sync_status=SYNC_STATUS.NEED_SYNC)
        obj.save()

    def changelist_view(self, request, extra_context=None):
        if self.has_view_permission(request, None):
            self.has_change = True
        if not extra_context:
            extra_context = {}
        extra_context.update({
            'has_change_permission': request.user.has_perm(self.opts.app_label + '.' + self.opts.get_change_permission())
        })
        extra_context.update({'has_sync_to_permission': self.has_sync_to_permission(request)})
        extra_context.update({'has_sync_from_permission': self.has_sync_from_permission(request)})
        result = super(BaseModelAdmin, self).changelist_view(request, extra_context=extra_context)
        self.has_change = False
        return result

    def has_view_permission(self, request, obj=None):
        opts = self.opts
        view_permission = 'view_%s' % self.model._meta.model_name
        return request.user.has_perm(opts.app_label + '.' + view_permission)

    def has_change_permission(self, request, obj=None):
        if getattr(self, 'has_change', False):
            return True
        return super(BaseModelAdmin, self).has_change_permission(request, obj)

    def add_view(self, request, form_url='', extra_context=None):
        self.in_add_view = True
        result = super(BaseModelAdmin, self).add_view(request, form_url, extra_context)
        self.in_add_view = False
        return result

    def change_view(self, request, object_id, extra_context=None):
        if self.has_view_permission(request, None):
            self.has_change = True
        result = super(BaseModelAdmin, self).change_view(request, object_id, extra_context=extra_context)
        self.has_change = False
        return result

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        old_has_change = self.has_change
        self.has_change = False
        context.update({'has_sync_to_permission': self.has_sync_to_permission(request)})
        result = super(BaseModelAdmin, self).render_change_form(request, context, add=add,
                                                                change=change, form_url=form_url, obj=obj)
        if old_has_change:
            self.has_change = True
        return result

    def save_formset(self, request, form, formset, change):
        """
        Given an inline formset save it to the database.
        """
        if request.method == "POST":
            objs = formset.save(commit=False)
            for obj in objs:
                if not obj.pk:    # new
                    obj.creator = request.user
                    obj.created_time = datetime.datetime.now()
                obj.modified_time = datetime.datetime.now()
                obj.modifier = request.user
                obj.sync_status = 0
                obj.save()
            formset.save_m2m()

    def get_form(self, request, obj=None, **kwargs):
        if self.in_add_view:
            if 'exclude' in kwargs:
                kwargs['exclude'] += self.special_exclude
            else:
                kwargs['exclude'] = self.special_exclude
        return super(BaseModelAdmin, self).get_form(request, obj, **kwargs)

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if request.method == "GET":
                kwargs = {'exclude': self.special_exclude}
                yield inline.get_formset(request, obj, **kwargs)
            else:
                yield inline.get_formset(request, obj)

    def _declared_fieldsets(self):
        if self.in_add_view:
            return super(BaseModelAdmin, self)._declared_fieldsets()
        else:
            if self.fieldsets:
                return self.fieldsets + self.special_fieldset
            elif self.fields:
                return [(None, {'fields': self.fields})]
            return None
    declared_fieldsets = property(_declared_fieldsets)

    def get_readonly_fields(self, request, obj=None):
        if not self.in_add_view:
            self.special_readonly += self.readonly_fields
            return self.special_readonly
        return ()

    def response_change(self, request, obj):
        opts = obj._meta
        verbose_name = opts.verbose_name
        if obj._deferred:
            opts_ = opts.proxy_for_model._meta
            verbose_name = opts_.verbose_name
        return_url = request.GET.get('rtn_url', None)

        if '_saveandsync' in request.POST:
            sync_obj(obj, self.model)
            self.message_user(
                request,
                (_("The %(name)s \"%(obj)s\" was changed successfully, and successfully synced to production.") %
                    {'name': force_unicode(verbose_name), 'obj': force_unicode(obj)})
            )
            return HttpResponseRedirect("../")
        elif '_continue' not in request.POST and '_saveasnew' not in request.POST \
                and "_addanother" not in request.POST and self.has_change_permission(request, None) and return_url:
            msg = _('The %(name)s "%(obj)s" was changed successfully.') % {'name': force_unicode(verbose_name), 'obj': force_unicode(obj)}
            self.message_user(request, msg)
            return HttpResponseRedirect(return_url)
        else:
            return super(BaseModelAdmin, self).response_change(request, obj)

    def response_add(self, request, obj, post_url_continue='../%s/'):
        if "_saveandsync" in request.POST:
            sync_obj(obj, self.model)
            self.message_user(
                request,
                (_("The %(name)s \"%(obj)s\" was added successfully, and successfully synced to production.") %
                    {'name': force_unicode(obj._meta.verbose_name), 'obj': force_unicode(obj)})
            )
            return HttpResponseRedirect("../")
        else:
            return super(BaseModelAdmin, self).response_add(request, obj)


class StackedInline(admin.StackedInline):
    extra = 1
    exclude = ('creator', 'created_time', 'modifier', 'modified_time', 'sync_status')
    template = 'admin/edit_inline/stacked.html'


class TabularInline(admin.TabularInline):
    extra = 1
    exclude = ('creator', 'created_time', 'modifier', 'modified_time', 'sync_status')
    template = 'admin/edit_inline/tabular.html'
