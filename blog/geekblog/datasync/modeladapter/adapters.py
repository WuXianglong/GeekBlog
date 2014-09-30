#! -*- coding:utf-8 -*-
import logging

from geekblog.utils import safe_cast
from geekblog.mongodb import datetime2timestamp, timestamp2datetime

logger = logging.getLogger('geekblog')


class ModelAdapter(object):

    def __init__(self, conn_ops):
        self.conn_ops = conn_ops

    def convert_to(self, from_model):
        pass

    def convert_from(self, to_model, data):
        pass


class CategoryAdapter(ModelAdapter):

    def convert_to(self, from_model):
        try:
            return {
                'id': from_model.id,
                'name': from_model.name,
                'slug': from_model.slug,
                'description': from_model.description,
                'icon_url': from_model.icon_path.url if from_model.icon_path else from_model.icon_url,
                'parent_id': from_model.parent.id if from_model.parent else 0,
                'has_child': from_model.children.count() > 0,
                'article_count': from_model.article_counts(),
                'views_count': from_model.views_count,
            }
        except Exception, e:
            logger.exception('Convert category failed, error: %s' % e)
            return {}


class TagAdapter(ModelAdapter):

    def convert_to(self, from_model):
        try:
            return {
                'id': from_model.id,
                'name': from_model.name,
                'slug': from_model.slug,
                'views_count': from_model.views_count,
                'article_count': from_model.total_articles.filter(hided=False).count(),
            }
        except Exception, e:
            logger.exception('Convert tag failed, error: %s' % e)
            return {}


class LinkAdapter(ModelAdapter):

    def convert_to(self, from_model):
        try:
            return {
                'id': from_model.id,
                'type': from_model.type,
                'title': from_model.title,
                'icon_url': from_model.icon_url,
                'address': from_model.address,
                'description': from_model.description,
            }
        except Exception, e:
            logger.exception('Convert link failed, error: %s' % e)
            return {}


class SliderAdapter(ModelAdapter):

    def convert_to(self, from_model):
        try:
            return {
                'id': from_model.id,
                'title': from_model.title,
                'jump_url': from_model.jump_url,
                'image_url': (from_model.image.path.url if from_model.image.path else from_model.image.url) if from_model.image else 'http://xianglong.qiniudn.com/default_slider_image.gif',
                'description': from_model.description,
            }
        except Exception, e:
            logger.exception('Convert slider failed, error: %s' % e)
            return {}


class ArticleAdapter(ModelAdapter):

    def convert_to(self, from_model):
        try:
            return {
                'id': from_model.id,
                'title': from_model.title,
                'slug': from_model.slug,
                'parent_cate_id': from_model.category.parent.id,
                'category_id': from_model.category.id,
                'category_name': from_model.category.name,
                'category_slug': from_model.category.slug,
                'description': from_model.description,
                'content': from_model.content,
                'mark': from_model.mark,
                'enable_comment': from_model.enable_comment,
                'login_required': from_model.login_required,
                'views_count': from_model.views_count,
                'comment_count': from_model.comment_count,    # TODO: get from comment model?
                'publish_date': datetime2timestamp(from_model.publish_date, convert_to_utc=True),
                'thumbnail_url': (from_model.thumbnail.path.url if from_model.thumbnail.path else from_model.thumbnail.url) if from_model.thumbnail else 'http://xianglong.qiniudn.com/default_article_image.gif',
                'tags': from_model.get_tags(),
                'tag_ids': [tag.id for tag in from_model.tags.all()],
            }
        except Exception, e:
            logger.exception('Convert article failed, error: %s' % e)
            return {}


class CommentAdapter(ModelAdapter):

    def convert_to(self, from_model):
        try:
            return {
                'id': from_model.id,
                'user_id': from_model.user.id if from_model.user else 0,
                'username': from_model.user.username if from_model.user else '',
                'article_id': from_model.article.id,
                'author': from_model.author,
                'author_email': from_model.author_email,
                'author_website': from_model.author_website,
                'author_ip': from_model.author_ip,
                'author_agent': from_model.author_agent,
                'parent_id': from_model.parent.id if from_model.parent else 0,
                'comment_date': datetime2timestamp(from_model.comment_date, convert_to_utc=True),
                'content': from_model.content,
            }
        except Exception, e:
            logger.exception('Convert comment failed, error: %s' % e)
            return {}

    def convert_from(self, to_model, data):
        if safe_cast(data.get('user_id', 0), int):
            to_model.user_id = int(data['user_id'])
        else:
            to_model.user = None
        if safe_cast(data.get('article_id', 0), int):
            to_model.article_id = int(data['article_id'])
        else:
            to_model.article = None
        if safe_cast(data.get('parent_id', 0), int):
            to_model.parent_id = int(data['parent_id'])
        else:
            to_model.comment = None
        to_model.author = data.get('author', '')
        to_model.author_email = data.get('author_email', '')
        to_model.author_website = data.get('author_website', '')
        to_model.author_ip = data.get('author_ip', '')
        to_model.author_agent = data.get('author_agent', '')
        to_model.comment_date = timestamp2datetime(data.get('comment_date', 0), convert_to_local=True)
        to_model.content = data.get('content', '')
        to_model.status = 1
        return to_model
