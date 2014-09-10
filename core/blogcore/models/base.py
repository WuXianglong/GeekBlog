# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from blogcore.models.constants import SYNC_STATUS


class BaseManager(models.Manager):
    """
    Base manager.
    options: queryset filter options
    """
    def __init__(self, options={}):
        self.options = options
        super(BaseManager, self).__init__()

    def get_query_set(self):
        query_set = super(BaseManager, self).get_query_set().filter(hided=False).filter(**self.options)
        return query_set.distinct()


class BaseModel(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("creator"))
    created_time = models.DateTimeField(verbose_name=_("created_time"))
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("modifier"), related_name="+")
    modified_time = models.DateTimeField(verbose_name=_("last modified"))
    hided = models.BooleanField(default=False, verbose_name=_("hided"))
    # used to decide to delete or update data in mongo when run syncto actioin.
    published = models.BooleanField(default=False, verbose_name=_("published"))
    sync_status = models.IntegerField(default=0, choices=SYNC_STATUS.to_choices(), verbose_name=_("sync status"))
    order = models.IntegerField(null=True, blank=True, verbose_name=_('No.'))

    objects = BaseManager()

    def modifier_name(self):
        if self.pk:
            return self.modifier.username
        return None
    modifier_name.short_description = _('modifier')

    def creator_name(self):
        if self.pk:
            return self.creator.username
        return None
    creator_name.short_description = _('creator')

    def delete(self):
        self.hided = 1
        self.sync_status = 0
        self.save()

    class Meta:
        abstract = True
