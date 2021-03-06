"""
Admin ui common utilities.
"""
import warnings
from fnmatch import fnmatch

from django.conf import settings
from django.core.urlresolvers import reverse

from admin_tools.sites import custom_site


def get_admin_site_name(context):
    return custom_site.name


def get_avail_models(request):
    """ Returns (model, perm,) for all models user can possibly see """
    items = []
    admin_site = custom_site

    for model, model_admin in admin_site._registry.items():
        perms = model_admin.get_model_perms(request)
        if True not in perms.values():
            continue
        items.append((model, perms,))
    return items


def filter_models(request, models, exclude):
    """
    Returns (model, perm,) for all models that match models/exclude patterns
    and are visible by current user.
    """
    items = get_avail_models(request)
    included = []
    full_name = lambda model: '%s.%s' % (model.__module__, model.__name__)

    # I beleive that that implemented
    # O(len(patterns)*len(matched_patterns)*len(all_models))
    # algorythm is fine for model lists because they are small and admin
    # performance is not a bottleneck. If it is not the case then the code
    # should be optimized.

    if len(models) == 0:
        included = items
    else:
        for pattern in models:
            for item in items:
                model, perms = item
                if fnmatch(full_name(model), pattern) and item not in included:
                    included.append(item)

    result = included[:]
    for pattern in exclude:
        for item in included:
            model, perms = item
            if fnmatch(full_name(model), pattern):
                try:
                    result.remove(item)
                except ValueError:  # if the item was already removed skip
                    pass
    return result


class AppListElementMixin(object):
    """
    Mixin class used by both the AppListDashboardModule and the
    AppListMenuItem (to honor the DRY concept).
    """

    def _visible_models(self, request):
        # compatibility layer: generate models/exclude patterns
        # from include_list/exclude_list args

        if self.include_list:
            warnings.warn(
               "`include_list` is deprecated for ModelList and AppList and "
               "will be removed in future releases. Please use `models` instead.",
               DeprecationWarning
            )

        if self.exclude_list:
            warnings.warn(
               "`exclude_list` is deprecated for ModelList and AppList and "
               "will be removed in future releases. Please use `exclude` instead.",
               DeprecationWarning
            )

        included = self.models[:]
        included.extend([elem + "*" for elem in self.include_list])

        excluded = self.exclude[:]
        excluded.extend([elem + "*" for elem in self.exclude_list])
        if self.exclude_list and not included:
            included = ["*"]
        return filter_models(request, included, excluded)

    def _get_admin_app_list_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse('%s:app_list' % get_admin_site_name(context),
                       args=(app_label,))

    def _get_admin_change_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_changelist' % (get_admin_site_name(context),
                                                app_label,
                                                model.__name__.lower()))

    def _get_admin_add_url(self, model, context):
        """
        Returns the admin add url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_add' % (get_admin_site_name(context),
                                         app_label,
                                         model.__name__.lower()))


def get_media_url():
    """
    Returns the django admin tools media URL.
    """
    media_url = getattr(settings, 'ADMIN_TOOLS_MEDIA_URL', None)
    if media_url is None:
        media_url = getattr(settings, 'STATIC_URL', None)
    if media_url is None:
        media_url = getattr(settings, 'MEDIA_URL')
    return media_url.rstrip('/')
