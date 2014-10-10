from django.utils.translation import ugettext as _
from django.db.models.base import ModelBase

from geekblog.utils import StringWithTitle
from geekblog.admin_tools.management import create_permission
from geekblog.blog.models import BaseManager, Article, Category

CATEGORIES = {}


def get_category(cate_name, only_id=False):
    if cate_name not in CATEGORIES:
        try:
            category = Category.objects.get(name=cate_name, parent__isnull=True)
            CATEGORIES[cate_name] = category
        except:
            pass
    cate = CATEGORIES.get(cate_name, None)
    return cate.id if cate and only_id else cate


def query_categories(only_id=False):
    categories = Category.objects.filter(parent__id=None)
    for cate in categories:
        CATEGORIES[cate.name] = cate
    return [c.id for c in categories] if only_id else categories


def catearticle_factory(class_s, category_name, model=Article):

    def _get_meta(category_name):
        class Meta:
            proxy = True
            app_label = StringWithTitle('catearticles', _('Category Articles'))
            verbose_name = category_name
            verbose_name_plural = category_name
        return Meta

    class_attrs = {
        'Meta': _get_meta(category_name),
        '__module__': __name__,
        'objects': BaseManager({'category__id__in': get_category(category_name).get_children(only_id=True)})
    }
    class_name = '%s%s' % (model.__name__, class_s)
    model_class = ModelBase(class_name, (model,), class_attrs)
    create_permission(model_class)

    return model_class
