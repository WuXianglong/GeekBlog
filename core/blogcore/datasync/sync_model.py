import sys
import traceback
from django.conf import settings

from blogcore.datasync.modeladapter import get_adapter


def sync_obj(obj, cls):
    adapter = get_adapter(cls)
    db_conn = adapter.conn_ops['db'](settings.MONGODB_CONF)
    update_table = adapter.conn_ops['table']

    to_obj = adapter.convert_to(obj)
    cond = {'pk': to_obj['pk']} if 'pk' in to_obj else {'id': to_obj['id']}
    if obj.published:
        try:
            db_conn.upsert_item(update_table, cond, to_obj, upsert=True)
        except:
            trace_stack = '\n'.join(traceback.format_exception(*sys.exc_info()))
            print 'cond: %s, obj:%s, e: %s' % (cond, to_obj, trace_stack)
    else:
        try:
            db_conn.delete_item(update_table, cond)
        except:
            trace_stack = '\n'.join(traceback.format_exception(*sys.exc_info()))
            print 'cond: %s, e: %s' % (cond, trace_stack)
    obj.sync_status = 1
    obj.save()
