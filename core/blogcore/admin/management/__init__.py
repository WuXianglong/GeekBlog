# -*- coding: utf-8 -*-
from django.db.models import get_models, signals
from django.utils.encoding import smart_unicode
from django.contrib.auth import models as auth_app
from django.contrib.auth.management import create_permissions

from blogcore.models.base import BaseModel
from blogcore.models.blog import Comment


def _get_permission_codename(action, opts):
    return u'%s_%s' % (action, opts.object_name.lower())


def _get_all_permissions(opts, actions):
    """ Returns (codename, name) for all permissions in the given opts. """
    perms = []
    for action in actions:
        perms.append((_get_permission_codename(action, opts), u'Can %s %s' % (action, opts.verbose_name_raw)))
    return perms


def _get_default_permissions(opts):
    return _get_all_permissions(opts, ('add', 'change', 'delete', 'view'))


def _get_sync_to_permissions(opts):
    return _get_all_permissions(opts, ('sync_to',))


def _get_sync_from_permissions(opts):
    return _get_all_permissions(opts, ('sync_from',))


def create_permissions_respecting_proxy(app, created_models, verbosity, **kwargs):
    from django.contrib.contenttypes.models import ContentType

    app_models = get_models(app)

    # This will hold the permissions we're looking for as
    # (content_type, (codename, name))
    searched_perms = list()
    # The codenames and ctypes that should exist.
    ctypes = set()
    for klass in app_models:
        ctype, created = ContentType.objects.get_or_create(
            app_label=klass._meta.app_label,
            model=klass._meta.model_name,
            defaults={'name': smart_unicode(klass._meta.verbose_name_raw)}
        )
        ctypes.add(ctype)
        for perm in _get_default_permissions(klass._meta):
            searched_perms.append((ctype, perm))
        if issubclass(klass, BaseModel) or issubclass(klass, Comment):
            for perm in _get_sync_to_permissions(klass._meta):
                searched_perms.append((ctype, perm))
        if issubclass(klass, Comment):
            for perm in _get_sync_from_permissions(klass._meta):
                searched_perms.append((ctype, perm))

    # Find all the Permissions that have a context_type for a model we're
    # looking for.  We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(auth_app.Permission.objects.filter(
        content_type__in=ctypes,
    ).values_list(
        "content_type", "codename"
    ))

    for ctype, (codename, name) in searched_perms:
        # If the permissions exists, move on.
        if (ctype.pk, codename) in all_perms:
            continue
        p = auth_app.Permission.objects.create(
            codename=codename,
            name=name,
            content_type=ctype
        )
        if verbosity >= 2:
            print "Adding permission '%s'" % p


def create_permission(model_class):
    from django.contrib.contenttypes.models import ContentType

    searched_perms = list()
    ctype, created = ContentType.objects.get_or_create(
        app_label=model_class._meta.app_label,
        model=model_class._meta.model_name,
        defaults={'name': smart_unicode(model_class._meta.verbose_name_raw)}
    )
    for perm in _get_default_permissions(model_class._meta):
        searched_perms.append(perm)
    if issubclass(model_class, BaseModel):
        for perm in _get_sync_to_permissions(model_class._meta):
            searched_perms.append(perm)

    # Find all the Permissions that have a context_type for a model we're
    # looking for.  We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(auth_app.Permission.objects.filter(
        content_type=ctype,
    ).values_list(
        "content_type", "codename"
    ))

    for (codename, name) in searched_perms:
        # If the permissions exists, move on.
        if (ctype.pk, codename) in all_perms:
            continue
        p = auth_app.Permission.objects.create(
            codename=codename,
            name=name,
            content_type=ctype
        )

signals.post_syncdb.disconnect(
    create_permissions,
    dispatch_uid='django.contrib.auth.management.create_permissions',
)
signals.post_syncdb.connect(
    create_permissions_respecting_proxy,
    dispatch_uid='django.contrib.auth.management.create_permissions',
)
