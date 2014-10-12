import logging
from django import forms

from blog.admin import ArticleAdmin
from admin_tools.sites import custom_site
from catearticles.models import get_category, query_categories, catearticle_factory

logger = logging.getLogger('geekblog')


class CategoryArticleAdmin(ArticleAdmin):

    def queryset(self, request):
        return super(CategoryArticleAdmin, self).queryset(request).filter(category__id__in=self.category.get_children(only_id=True))

    @property
    def category(self):
        return get_category(self.cate_name)

    def has_add_permission(self, request):
        return True

    def has_sync_to_permission(self, request, obj=None):
        return True


def catearticleadmin_factory(class_s, category_name, model=CategoryArticleAdmin):

    class_attrs = {
        'cate_name': category_name,
        '__module__': __name__,
    }
    class_name = '%s%s' % (model.__name__, class_s)
    return forms.MediaDefiningClass(class_name, (model,), class_attrs)


categories = query_categories()
for cate in categories:
    custom_site.register(catearticle_factory(cate.id, cate.name), catearticleadmin_factory(cate.id, cate.name))
