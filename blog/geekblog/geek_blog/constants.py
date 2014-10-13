#! -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _


class Enum(object):
    '''
    An enum type used in django convenience.

    >>> from enum import Enum
    >>> e = Enum({"ONE":(1,"One")})
    >>> print e.ONE
    1
    >>> print e.to_choices()
    ((1, 'One'),)
    >>> print e.to_dict()
    {1: 'One'}
    >>> print e.get_label(1)
    One
    >>> print e.get_key(1)
    ONE
    '''
    def __init__(self, mapping):
        self._DATA_MAPPING = mapping

    def __getattr__(self, name):
        if name in self._DATA_MAPPING:
            return self._DATA_MAPPING[name][0]
        return super(self, Enum).__getattr__(name)

    def to_choices(self):
        value_label_tuples = [self._DATA_MAPPING[key] for key in self._DATA_MAPPING]
        return tuple(value_label_tuples)

    def to_dict(self):
        value_label_dict = {}
        for key in self._DATA_MAPPING:
            value_label_dict[self._DATA_MAPPING[key][0]] = self._DATA_MAPPING[key][1]
        return value_label_dict

    def get_label(self, value):
        value_label_dict = self.to_dict()
        return value_label_dict[value]

    def get_key(self, value):
        for key in self._DATA_MAPPING:
            if self._DATA_MAPPING[key][0] == value:
                return key


ALL_MONTHS = [_('JAN'), _('FEB'), _('MAR'), _('APR'), _('MAY'), _('JUN'),
              _('JUL'), _('AUG'), _('SEP'), _('OCT'), _('NOV'), _('DEC')]

SYNC_STATUS = Enum({
    'NEED_SYNC': (0, _('Need Sync')),
    'SYNCED': (1, _('Synced')),
})

USER_STATUS = Enum({
    'NOT_AUTHED': (0, _('Not Authed')),
    'ACTIVE': (1, _('Active')),
    'REJECTED': (2, _('Rejected')),
})

ARTICLE_MARKS = Enum({
    'NEWEST': (0, _('Newest')),
    'HOTTEST': (1, _('Hottest')),
    'RECOMMEND': (2, _('Recommend')),
})

ARTICLE_STATUS = Enum({
    'DRAFT': (0, _('Not Reviewed')),
    'PUBLISHED': (1, _('Published')),
    'EXPIRED': (2, _('Expired')),
})

COMMENT_STATUS = Enum({
    'NOT_REVIEWED': (0, _('Not Reviewed')),
    'APPROVED': (1, _('Approved')),
    'REJECTED': (2, _('Rejected')),
})

LINK_TYPES = Enum({
    'FRIEND_LINK': (0, _("Friend's Links")),
    'SITE_LINK': (1, _("Site's Links")),
})
