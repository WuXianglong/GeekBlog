from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from blogcore.admin import BaseModelAdmin
from blogcore.admin.sites import custom_site
from blogcore.models.constants import ARTICLE_STATUS, COMMENT_STATUS
from blog.models import Category, Tag, Link, Slider, Photo, Article, Comment


class CategoryAdmin(BaseModelAdmin):
    readonly_fields = ('views_count',)
    list_editable = ('published', 'order')
    list_display = ('order', 'name', 'slug', 'description', 'parent', \
            'modified_time', 'published', 'sync_status')
    list_display_links = ('name',)
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_filter = ['published', 'sync_status']
    search_fields = ['name', 'slug', 'description']
    ordering = ('order',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('name', 'slug', 'description', 'parent', 'icon_url', 'icon_path'),
        }),
        (_('Status'), {
            'fields': ('published',),
        }),
    )


class TagAdmin(BaseModelAdmin):
    readonly_fields = ('views_count',)
    list_editable = ('published', 'order')
    list_display = ('order', 'name', 'slug', 'modified_time', 'published', 'sync_status')
    list_display_links = ('name',)
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_filter = ['published', 'sync_status']
    search_fields = ['name', 'slug']
    ordering = ('order',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('name', 'slug'),
        }),
        (_('Status'), {
            'fields': ('published',),
        }),
    )


class LinkAdmin(BaseModelAdmin):
    list_editable = ('published', 'order')
    list_display = ('order', 'title', 'address', 'icon_url', 'modified_time', \
            'published', 'sync_status')
    list_display_links = ('title',)
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_filter = ['type', 'published', 'sync_status']
    search_fields = ['title', 'address']
    ordering = ('order',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('type', 'title', 'address', 'icon_url', 'description'),
        }),
        (_('Status'), {
            'fields': ('published',),
        }),
    )


class SliderAdmin(BaseModelAdmin):
    list_editable = ('published', 'order')
    list_display = ('order', 'title', 'description', 'modified_time', 'published', 'sync_status')
    list_display_links = ('title',)
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_filter = ['published', 'sync_status']
    search_fields = ['title', 'description']
    ordering = ('order',)
    raw_id_fields = ('image',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('title', 'image', 'jump_url', 'description'),
        }),
        (_('Status'), {
            'fields': ('published',),
        }),
    )


class PhotoAdmin(BaseModelAdmin):
    list_editable = ('published', 'order')
    list_display = ('order', 'id', 'title', 'url', 'path', 'modified_time', 'published', 'sync_status')
    list_display_links = ('id',)
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    search_fields = ['title', 'path']
    ordering = ('order',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('title', 'url', 'path'),
        }),
        (_('Status'), {
            'fields': ('published',),
        }),
    )

    def has_sync_to_permission(self, request, obj=None):
        return False


class ArticleAdmin(BaseModelAdmin):
    readonly_fields = ('views_count', 'comment_count')
    list_editable = ('order', 'status', 'enable_comment', 'login_required', 'published')
    list_display = ('order', 'title', 'slug', 'category', 'status', 'enable_comment', \
            'display_tags', 'publish_date', 'modified_time', 'login_required', 'published', 'sync_status')
    list_display_links = ('title',)
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_filter = ['status', 'mark', 'enable_comment', 'sync_status']
    search_fields = ['title', 'slug', 'description']
    ordering = ('order',)
    raw_id_fields = ('thumbnail',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('title', 'slug', 'category', 'thumbnail', 'publish_date', 'tags', 'description', 'content'),
        }),
        (_('Status'), {
            'fields': ('mark', 'status', 'enable_comment', 'login_required', 'published'),
        }),
    )

    def _can_published_or_not(self, obj):
        if obj.status == ARTICLE_STATUS.PUBLISHED:
            return True, ''
        else:
            return False, _("You can't publish not approved %(model)s: %(obj)s") \
                    % {'model': self.model._meta.verbose_name, 'obj': obj}

    def _get_need_adjust_items(self, request, old_obj, new_obj):
        order_is_existed = self.queryset(request).filter(category__exact=new_obj.category, order__exact=new_obj.order)
        # if new order is not existed before, return
        if not order_is_existed:
            [], 0
        # if the model is new, set old_order using _get_next_order
        if old_obj:
            old_order, new_order = old_obj.order, new_obj.order
        else:
            old_order, new_order = self._get_next_order(request), new_obj.order
        if new_order > old_order:    # order reduce
            need_adjust_items = self.queryset(request).filter(category__exact=new_obj.category, \
                    order__gt=old_order, order__lte=new_order)
            adjust_amount = -1
        else:    # order rise
            need_adjust_items = self.queryset(request).filter(category__exact=new_obj.category, \
                    order__gte=new_order, order__lt=old_order)
            adjust_amount = 1
        return need_adjust_items, adjust_amount


class CommentAdmin(BaseModelAdmin):
    list_editable = ('status', 'published')
    list_display = ('author', 'user', 'article', 'author_email', 'comment_date', 'status', \
            'content', 'published', 'sync_status')
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_filter = ['status', 'published']
    search_fields = ['author', 'author_email', 'content']
    ordering = ('-comment_date',)
    raw_id_fields = ('user', 'article')
    fieldsets = (
        (_('Basic'), {
            'fields': ('user', 'article', 'author', 'author_email', 'author_website', 'author_ip', \
                        'author_agent', 'parent', 'comment_date', 'content'),
        }),
        (_('Status'), {
            'fields': ('status', 'published'),
        }),
    )
    special_exclude = ('sync_status',)
    special_readonly = ('sync_status',)

    def save_model(self, request, obj, form, change):
        obj.sync_status = 0
        obj.save()

    def save_formset(self, request, form, formset, change):
        """
        Given an inline formset save it to the database.
        """
        if request.method == "POST":
            objs = formset.save(commit=False)
            for obj in objs:
                obj.sync_status = 0
                obj.save()
            formset.save_m2m()

    def has_sync_to_permission(self, request, obj=None):
        return False

    def has_sync_from_permission(self, request, obj=None):
        return False

    def _can_published_or_not(self, obj):
        if obj.status == COMMENT_STATUS.APPROVED:
            return True, ''
        else:
            return False, _("You can't publish not approved %(model)s: %(obj)s") \
                    % {'model': self.model._meta.verbose_name, 'obj': obj}

custom_site.register(Category, CategoryAdmin)
custom_site.register(Tag, TagAdmin)
custom_site.register(Link, LinkAdmin)
custom_site.register(Slider, SliderAdmin)
custom_site.register(Photo, PhotoAdmin)
custom_site.register(Article, ArticleAdmin)
custom_site.register(Comment, CommentAdmin)
