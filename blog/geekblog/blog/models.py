# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _

from utils import StringWithTitle
from ueditor.models import UEditorField
from admin_tools.storages import LocalFileSystemStorage
from geek_blog.constants import SYNC_STATUS, ARTICLE_MARKS, ARTICLE_STATUS, COMMENT_STATUS, LINK_TYPES


def _get_cate_children(category, only_id=False):
    children = []
    for child in category.children.all():
        if only_id:
            children.append(child.id)
            if child.children.count():
                children.extend(child.get_children(only_id=True))
        else:
            children.append(child)
            if child.children.count():
                children.extend(child.get_children(only_id=False))
    return children


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


class Category(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    slug = models.CharField(max_length=100, unique=True, verbose_name=_('slug'))
    description = models.TextField(max_length=4096, verbose_name=_('description'))
    icon_url = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name=_('icon URL'))
    icon_path = models.ImageField(storage=LocalFileSystemStorage(), upload_to='upload/images/', verbose_name=_('icon path'),
                                  null=True, blank=True, help_text=_('Please upload JPEG, PNG, GIF files, size: 64x64'))
    # parent_category is null means top category
    parent = models.ForeignKey('self', related_name='children', limit_choices_to={'parent__isnull': True},
                               null=True, blank=True, default=None, verbose_name=_('parent category'))
    views_count = models.IntegerField(default=0, verbose_name=_('views count'))

    def __unicode__(self):
        if self.parent:
            return '%s -> %s' % (self.parent.name, self.name)
        return self.name

    def article_counts(self):
        if self.pk:
            count = 0
            for child in self.children.all():
                count += child.article_counts()
            return count + self.total_articles.filter(hided=False).count()
        return 0
    article_counts.short_description = _('article count')

    def get_children(self, only_id=False):
        return _get_cate_children(self, only_id=only_id)

    class Meta:
        app_label = StringWithTitle('blog', _('Blog'))
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        unique_together = ("name", "parent")


class Tag(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('name'))
    slug = models.CharField(max_length=100, unique=True, verbose_name=_('slug'))
    views_count = models.IntegerField(default=0, verbose_name=_('views count'))

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = StringWithTitle('blog', _('Blog'))
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Link(BaseModel):
    type = models.IntegerField(choices=LINK_TYPES.to_choices(), verbose_name=_('link type'))
    title = models.CharField(max_length=100, verbose_name=_('title'))
    icon_url = models.CharField(max_length=255, verbose_name=_('icon URL'))
    address = models.URLField(max_length=200, unique=True, verbose_name=_('address'))
    description = models.TextField(max_length=4096, verbose_name=_('description'))

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = StringWithTitle('blog', _('Blog'))
        verbose_name = _('Link')
        verbose_name_plural = _('Links')


class Photo(BaseModel):
    url = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name=_('icon URL'))
    path = models.ImageField(storage=LocalFileSystemStorage(), upload_to='upload/images/', null=True, blank=True, verbose_name=_('image path'))
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('image title'))

    def __unicode__(self):
        return self.title or self.path.name

    def save(self):
        if self.path:
            self.path.name = smart_str(self.path.name)
        self.published = 1
        self.sync_status = 1
        super(Photo, self).save()

    class Meta:
        app_label = StringWithTitle('blog', _('Blog'))
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')


class Slider(BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    image = models.ForeignKey(Photo, verbose_name=_('slider image'))
    jump_url = models.URLField(max_length=255, verbose_name=_('jump url'))
    description = models.TextField(max_length=2048, verbose_name=_('description'))

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = StringWithTitle('blog', _('Blog'))
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')


class Article(BaseModel):
    title = models.CharField(max_length=100, unique=True, verbose_name=_('title'))
    slug = models.CharField(max_length=100, unique=True, verbose_name=_('slug'))
    category = models.ForeignKey(Category, related_name='total_articles', limit_choices_to={'parent__isnull': False},
                                 verbose_name=_('category'))
    status = models.IntegerField(default=0, choices=ARTICLE_STATUS.to_choices(), verbose_name=_('status'))
    enable_comment = models.BooleanField(default=True, verbose_name=_('enable comment'))
    description = UEditorField(height=200, width=690, verbose_name=_('description'), null=True, blank=True,
                               toolbars='full', image_path="upload/images/", file_path='upload/files/')
    content = UEditorField(height=400, width=690, verbose_name=_('content'), toolbars='full',
                           image_path="upload/images/", file_path='upload/files/')
    mark = models.IntegerField(default=0, choices=ARTICLE_MARKS.to_choices(), verbose_name=_('mark'))
    tags = models.ManyToManyField(Tag, verbose_name=_('tag'), help_text=_('Tags that describe this article'),
                                  blank=True, related_name='total_articles')
    publish_date = models.DateTimeField(verbose_name=_('publish date'), help_text=_('The date and time this shall appear online.'))
    login_required = models.BooleanField(blank=True, verbose_name=_('login required'),
                                         help_text=_('Enable this if users must login before they can read this article.'))
    thumbnail = models.ForeignKey(Photo, null=True, blank=True, verbose_name=_('thumbnail'))
    views_count = models.IntegerField(default=0, verbose_name=_('views count'))
    comment_count = models.IntegerField(default=0, verbose_name=_('comment count'))

    def __unicode__(self):
        return self.title

    def get_tags(self):
        tags = []
        for tag in self.tags.all():
            tags.append({'id': tag.id, 'name': tag.name, 'slug': tag.slug})
        return tags

    def display_tags(self):
        tag_names = [tag['name'] for tag in self.get_tags()]
        return ', '.join(tag_names)
    display_tags.short_description = _('tags')

    def get_absolute_url(self):
        return "/console/article_preview/%s/" % self.slug

    class Meta:
        app_label = StringWithTitle('blog', _('Blog'))
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, verbose_name=_('user'))
    article = models.ForeignKey(Article, related_name='comments', verbose_name=_('article'))
    author = models.CharField(max_length=100, verbose_name=_('author'))
    author_email = models.CharField(max_length=100, verbose_name=_('email'))
    author_website = models.CharField(max_length=512, null=True, blank=True, verbose_name=_('website'))
    author_ip = models.CharField(max_length=100, verbose_name=_('ip'))
    author_agent = models.CharField(max_length=1024, verbose_name=_('user agent'))
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, default=None, verbose_name=_('parent comment'))
    comment_date = models.DateTimeField(verbose_name=_('comment date'))
    content = models.TextField(verbose_name=_('content'))
    hided = models.BooleanField(default=False, verbose_name=_("hided"))
    published = models.BooleanField(default=False, verbose_name=_("published"))
    sync_status = models.IntegerField(default=0, choices=SYNC_STATUS.to_choices(), verbose_name=_("sync status"))
    status = models.IntegerField(default=COMMENT_STATUS.APPROVED, choices=COMMENT_STATUS.to_choices(), verbose_name=_('status'))
    duoshuo_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('duoshuo comment ID'))
    duoshuo_user_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('duoshuo user ID'))

    objects = BaseManager()

    def __unicode__(self):
        return self.article.title

    class Meta:
        app_label = StringWithTitle('blog', _('Blog'))
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
