#! -*- coding:utf-8 -*-
from syncto import sync_to_production
from syncfrom import sync_from_production

from mongodb.blog import BlogMongodbStorage
from blog.models import Category, Tag, Link, Slider, Article, Comment
from datasync.modeladapter import register, adapters

register(Category, adapters.CategoryAdapter, {'db': BlogMongodbStorage, 'table': 'categories'})
register(Tag, adapters.TagAdapter, {'db': BlogMongodbStorage, 'table': 'tags'})
register(Link, adapters.LinkAdapter, {'db': BlogMongodbStorage, 'table': 'links'})
register(Slider, adapters.SliderAdapter, {'db': BlogMongodbStorage, 'table': 'sliders'})
register(Article, adapters.ArticleAdapter, {'db': BlogMongodbStorage, 'table': 'articles'})
register(Comment, adapters.CommentAdapter, {'db': BlogMongodbStorage, 'table': 'comments', 'method': 'get_need_sync_comments'})
