from django.contrib.admin.views.main import ALL_VAR, PAGE_VAR
from django.template import Library
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

register = Library()
DOT = '.'


def paginator_number(cl, i):
    """
    Generates an individual page index link in a paginated list.
    """
    if i == DOT:
        return u'... '
    elif i == 'next':
        return mark_safe(u'<a href="%s" class="pagenav" id="next">%s</a> ' \
                % (escape(cl.get_query_string({PAGE_VAR: cl.page_num + 1})), _('next page')))
    elif i == 'last':
        return mark_safe(u'<a href="%s" class="pagenav" id="last">%s</a> ' \
                % (escape(cl.get_query_string({PAGE_VAR: cl.page_num - 1})), _('prev page')))
    else:
        return mark_safe(u'<a href="%s" class="pagenav %s">%d</a> ' \
                % (escape(cl.get_query_string({PAGE_VAR: i})), 'on' if i == cl.page_num else '', i + 1))

paginator_number = register.simple_tag(paginator_number)


def pagination(cl, has_change_permission):
    """
    Generates the series of links to the pages in a paginated list.
    """
    paginator, page_num = cl.paginator, cl.page_num
    current_page = paginator.page(page_num + 1)
    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page

    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 2 
        ON_ENDS = 1

        # If there are 10 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 10:
            page_range = range(paginator.num_pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > (ON_EACH_SIDE + ON_ENDS):
                page_range.extend(range(0, ON_EACH_SIDE - 1))
                page_range.append(DOT)
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
                page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.append(DOT)
                page_range.extend(range(paginator.num_pages - ON_ENDS, paginator.num_pages))
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))
    return {
        'cl': cl,
        'pagination_required': pagination_required,
        'ALL_VAR': ALL_VAR,
        '1': 1,
        'has_change_permission': has_change_permission,
        "previous": cl.page_num - 1 if current_page.has_previous() else 0,
        "has_previous": current_page.has_previous(),
        "next": cl.page_num + 1 if current_page.has_next() else page_num - 1,
        "has_next": current_page.has_next(),
        "page_range": page_range,
    }

pagination = register.inclusion_tag('admin/pagination.html')(pagination)
