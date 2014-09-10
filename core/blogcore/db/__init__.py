# -*- coding: utf-8 -*-
import random
import logging
import datetime
from bson.son import SON
from functools import wraps
from pymongo.cursor import Cursor
from pymongo import DESCENDING, ASCENDING
from pymongo import ReplicaSetConnection, ReadPreference, Connection

logger = logging.getLogger('blogcore')
EPOCH = datetime.datetime(1970, 1, 1)


def set_default_order(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'order' not in kwargs or kwargs['order'] is None:
            kwargs['order'] = args[0].DEFAULT_ORDER
        return func(*args, **kwargs)
    return wrapper


def cursor_to_list(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retval = func(*args, **kwargs)
        if isinstance(retval, Cursor):
            retval = [x for x in retval]
        elif isinstance(retval, dict) and 'results' in retval and 'total' in retval:
            if isinstance(retval['results'], Cursor):
                retval['results'] = [x for x in retval['results']]
        return retval
    return wrapper


def total_seconds(delta):
    """ return total seconds of a time delta. """
    if not isinstance(delta, datetime.timedelta):
        raise TypeError('delta must be a datetime.timedelta.')
    return delta.days * 86400 + delta.seconds + delta.microseconds / 1000000.0


def datetime2timestamp(dt, convert_to_utc=False):
    ''' Converts a datetime object to UNIX timestamp in milliseconds. '''
    if isinstance(dt, datetime.datetime):
        if convert_to_utc:
            dt = dt + datetime.timedelta(hours=-8)
        timestamp = total_seconds(dt - EPOCH)
        return long(timestamp)
    return dt


def timestamp2datetime(timestamp, convert_to_local=False):
    ''' Converts UNIX timestamp to a datetime object. '''
    if isinstance(timestamp, (int, long, float)):
        dt = datetime.datetime.utcfromtimestamp(timestamp)
        if convert_to_local:
            dt = dt + datetime.timedelta(hours=8)
        return dt
    return timestamp


def timestamp_utc_now():
    return datetime2timestamp(datetime.datetime.utcnow())


def timestamp_now():
    return datetime2timestamp(datetime.datetime.now())


def get_last_sync_timestamp(model_class):
    items = model_class.objects.order_by('-created_time')
    return datetime2timestamp(items[0].created_time if items else EPOCH, convert_to_utc=True)


def weighted_sample(items, n):
    '''
    http://stackoverflow.com/questions/2140787/select-random-k-elements-from-a-list-whose-elements-have-weights/2149533#2149533
    '''
    selected = []
    if n < 0:
        return []
    if len(items) <= n:
        selected = [v for _, v in items]
    else:
        if n > 2:
            selected = [v for _, v in reversed(sorted(items, key=lambda x: x[0]))][:n]
        else:
            total = float(sum(w for w, _ in items))
            i = 0
            w, v = items[0]
            while n:
                x = total * (1 - random.random() ** (1.0 / n))
                total -= x
                while x > w:
                    x -= w
                    i += 1
                    w, v = items[i]
                w -= x
                selected.append(v)    # v maybe duplicated, if we filter duplicated v, when n big enough, request may timeout for while loop is not easy to endup.
                n -= 1
    return selected


class IncrementalId(object):
    """ implement incremental id for collection in mongodb. """

    def __init__(self, db):
        self.db = db
        self.colls = {}

    def _ensure_next_id(self, coll_name):
        """ ensure next_id item in collection ,if not, next_id method will throw exception rasie by pymongo """
        cond = {'_id': coll_name}
        id_info = self.db.ids.find_one(cond)
        if not id_info:
            self.db.ids.insert({'_id': coll_name, 'seq': 1L})

    def next_id(self, coll):
        """ get next increment id and increase it """
        if coll not in self.colls:
            self._ensure_next_id(coll)
        cond = {'_id': coll}
        update = {'$inc': {'seq': 1L}}
        son = SON([('findandmodify', 'ids'), ('query', cond), ('update', update), ('new', True)])
        seq = self.db.command(son)
        return seq['value']['seq']


class MongodbStorage(object):
    _db = None
    ORDER_ASC = ASCENDING
    ORDER_DESC = DESCENDING
    DEFAULT_ORDER = [("order", ORDER_ASC)]

    def __init__(self, conn_str, db_name):
        try:
            if conn_str.find("replicaSet") == -1:
                _conn = Connection(conn_str, max_pool_size=30, safe=True,
                                   read_preference=ReadPreference.SECONDARY_ONLY)
            else:
                _conn = ReplicaSetConnection(conn_str, max_pool_size=30, safe=True,
                                             read_preference=ReadPreference.SECONDARY_ONLY)
            self._db = _conn[db_name]
        except Exception, e:
            logger.exception('Can not connect to mongodb: %s' % e)
            raise e

    def delete_item(self, table, cond):
        eval('self._db.%s.remove(%s)' % (table, cond))

    def upsert_item(self, table, cond, item, upsert=False, multi=False):
        eval("self._db.%s.update(%s, {'$set': %s}, upsert=%s, multi=%s)" % (table, cond, item, upsert, multi))
