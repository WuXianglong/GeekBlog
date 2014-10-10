from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.text import Truncator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import ForeignKeyRawIdWidget


class CustomForeignKeyRawIdWidget(ForeignKeyRawIdWidget):

    def render(self, name, value, attrs=None):
        rel_to = self.rel.to
        if attrs is None:
            attrs = {}
        extra = []

        if rel_to in self.admin_site._registry:
            # The related object is registered with the same AdminSite
            related_url = reverse('admin:%s_%s_changelist' % (rel_to._meta.app_label, rel_to._meta.model_name),
                                  current_app=self.admin_site.name)
            params = self.url_parameters()
            if params:
                url = u'?' + u'&amp;'.join([u'%s=%s' % (k, v) for k, v in params.items()])
            else:
                url = u''
            if "class" not in attrs:
                attrs['class'] = 'vForeignKeyRawIdAdminField'    # The JavaScript looks for this hook.
            extra.append(u'<a href="%s%s" class="related-lookup" id="lookup_id_%s" onclick="return showRelatedObjectLookupPopup(this);"> ' %
                         (related_url, url, name))
            extra.append(u'<img src="%sadmin/img/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.STATIC_URL, _('Lookup')))
        output = [super(ForeignKeyRawIdWidget, self).render(name, value, attrs)] + extra
        output.append(self.label_for_value(value))
        return mark_safe(u''.join(output))

    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        obj_name = self.rel.to._meta.object_name
        related_url = reverse('admin:%s_%s_changelist' % (self.rel.to._meta.app_label, self.rel.to._meta.model_name), current_app=self.admin_site.name)

        if value:
            try:
                obj = self.rel.to._default_manager.using(self.db).get(**{key: value})
                return '&nbsp;<a href="%s%s/" cls_name="%s" target="_blank"><strong>%s</strong></a>' \
                        % (related_url, value, obj_name, escape(Truncator(obj).words(14, truncate='...')))
            except (ValueError, self.rel.to.DoesNotExist):
                return '&nbsp;<a href="" cls_name="" target="_blank"><strong></strong></a>'
        else:
            return '&nbsp;<a href="%sobj_id_placeholder/" cls_name="%s" target="_blank"><strong></strong></a>' \
                    % (related_url, obj_name)
