#! -*- coding:utf-8 -*-
import logging
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.util import model_ngettext

from blogcore.datasync.modeladapter import get_adapter

logger = logging.getLogger('geekblog')


def sync_to_production(modeladmin, request=None):
    adapter = get_adapter(modeladmin.model)
    db_conn = adapter.conn_ops['db'](settings.MONGODB_CONF)
    update_table = adapter.conn_ops['table']

    if request:
        need_sync_items = modeladmin.queryset(request).filter(sync_status=0)
    else:
        need_sync_items = modeladmin.model.objects.filter(sync_status=0)
    sync_successed = 0
    sync_failed = 0
    for i, obj in enumerate(need_sync_items):
        can_upsert = obj.published and not obj.hided
        to_obj = {}
        try:
            to_obj = adapter.convert_to(obj)
            if not to_obj:
                msg = 'convert to failed %s, id: %s' % (modeladmin.model, obj.pk)
                logger.warn(msg)
                sync_failed += 1
            else:
                cond = {'pk': to_obj['pk']} if 'pk' in to_obj else {'id': to_obj['id']}
                if can_upsert:
                    db_conn.upsert_item(update_table, cond, to_obj, upsert=True)
                else:
                    db_conn.delete_item(update_table, cond)
                obj.sync_status = 1
                obj.save()
                sync_successed += 1
        except Exception:
            msg = 'sync failed %s, id: %s' % (modeladmin.model, obj.pk)
            logger.exception(msg)
            sync_failed += 1

    success_msg = _("%(count)d %(items)s successfully sync data to production environment.\n") % {
                'count': sync_successed, 'items': model_ngettext(modeladmin.opts, sync_successed)
            }
    failed_msg = _("%(count)d %(items)s fail sync data to production environment.\n") % {
                'count': sync_failed, 'items': model_ngettext(modeladmin.opts, sync_failed)
            }
    if request:
        modeladmin.message_user(request, success_msg + failed_msg)
    else:
        print success_msg + failed_msg
