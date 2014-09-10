# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from blogcore.utils.enum import Enum

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
