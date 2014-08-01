#! -*- coding:utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.util import model_ngettext

from blogcore.datasync.modeladapter import get_adapter
from blogcore.db import get_last_sync_timestamp


def sync_from_production(modeladmin, request):
    model_cls = modeladmin.model
    adapter = get_adapter(model_cls)
    db_conn = adapter.conn_ops['db'](settings.MONGODB_CONF)

    start_time = get_last_sync_timestamp(model_cls)
    need_sync_items = getattr(db_conn, adapter.conn_ops['method'])(start_time)
    for item in need_sync_items:
        to_model = adapter.convert_from(model_cls(), item)
        to_model.save()
    count = len(need_sync_items)
    if count:
        modeladmin.message_user(request, _("%(count)d %(items)s successfully sync data from production environment.") % {
            'count': count, 'items': model_ngettext(modeladmin.opts, count)
        })
    else:
        modeladmin.message_user(request, _("No %(items)s need to sync to production environment.") % {
            'items': model_ngettext(modeladmin.opts, count),
        })
