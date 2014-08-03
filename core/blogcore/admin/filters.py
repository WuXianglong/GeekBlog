from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class ActionFlagFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('action flag')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'action_flag'

    action_values = {
        'add': 1,
        'change': 2,
        'delete': 3,
    }

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('add', _('addition action')),
            ('change', _('change action')),
            ('delete', _('deletion action')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # to decide how to filter the queryset.
        if self.value():
            return queryset.filter(action_flag__exact=self.action_values[self.value()])
