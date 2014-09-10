#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import logging
import datetime

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from blogcore.db.blog import BlogMongodbStorage
from blogcore.db import timestamp2datetime
from blogcore.models.blog import Article, Comment
from blogcore.models.constants import COMMENT_STATUS

blog_db = BlogMongodbStorage(settings.MONGODB_CONF)
logger = logging.getLogger('geekblog')


def _upsert_comment(comment):
    """
        操作类型:
            create：创建评论
            approve：通过评论
            spam：标记垃圾评论
            delete：删除评论
            delete-forever：彻底删除评论
    """
    action = comment.get('action', '')
    meta = comment.get('meta', None)
    if meta:
        try:
            if action == 'create':
                articles = Article.objects.filter(id=meta.get('thread_key', ''))
                if articles.count() == 0:
                    return
                c = Comment()
                c.article = articles[0]
                parent_id = meta.get('parent_id', '0')
                parent_c = Comment.objects.filter(duoshuo_id=parent_id)
                c.parent = None if parent_id == '0' or parent_c.count() == 0 else parent_c[0]

                c.duoshuo_id = meta.get('post_id', '')
                c.duoshuo_user_id = comment.get('user_id', '')
                c.author = meta.get('author_name', '')
                c.author_email = meta.get('author_email', '')
                c.author_website = meta.get('author_url', '')
                c.author_ip = meta.get('ip', '')
                c.comment_date = timestamp2datetime(comment.get('date', None), convert_to_local=True) or datetime.datetime.now()
                c.content = meta.get('message', '')
                c.author_agent = ''
                status = meta.get('status', '')
                c.status = COMMENT_STATUS.APPROVED if status == 'approved' else (COMMENT_STATUS.NOT_REVIEWED if status == 'pending' else COMMENT_STATUS.REJECTED)
                c.save()
            elif action == 'approve':
                Comment.objects.filter(duoshuo_id__in=meta).update(status=COMMENT_STATUS.APPROVED)
            elif action == 'spam':
                Comment.objects.filter(duoshuo_id__in=meta).update(status=COMMENT_STATUS.REJECTED)
            elif action in ('delete', 'delete-forever'):
                Comment.objects.filter(duoshuo_id__in=meta).update(hided=True, status=COMMENT_STATUS.REJECTED)
        except Exception, e:
            logger.exception('update article comment failed, exception: %s, comment: %s' % (e, comment))


class Command(BaseCommand):

    def handle(self, action='all', **options):
        print 'sync comment, views_count and comment_count'
        # sync views_count from mongodb
        articles = blog_db.get_articles({}, count=10000, fields={'_id': 0, 'id': 1, 'views_count': 1}, has_login=True)
        for article in articles:
            try:
                Article.objects.filter(id=article['id']).update(views_count=article['views_count'])
            except Exception, e:
                logger.exception('sync article views_count failed, exception: %s' % e)

        # sync article comments from duoshuo
        # API example: http://dev.duoshuo.com/docs/50037b11b66af78d0c000009
        try:
            api_params = {
                'short_name': getattr(settings, 'DUOSHUO_SHORT_NAME', ''),
                'secret': getattr(settings, 'DUOSHUO_SECRET', ''),
                'since_id': blog_db.get_last_log_id(),
                'limit': 200,
            }
            while True:
                r = requests.get('http://api.duoshuo.com/log/list.json', params=api_params)
                ret_msg = r.json()
                # if return error or return data length is 0, break
                if ret_msg['code'] != 0 or 'response' not in ret_msg or len(ret_msg['response']):
                    break
                for i, comment in enumerate(ret_msg['response']):
                    # update since_id for while loop
                    if i == len(ret_msg['response']) - 1:
                        api_params['since_id'] = comment['log_id']
                    # update or insert comment
                    _upsert_comment(comment)
            # save sync log_id
            blog_db.save_sync_log_id({'log_id': api_params['since_id'], 'sync_time': int(time.time())})
        except Exception, e:
            logger.exception('sync article comment from duoshuo failed, exception: %s' % e)

        # update article comment count
        for article in Article.objects.all().filter(hided=False):
            try:
                article.comment_count = article.comments.all().filter(hided=False, status=COMMENT_STATUS.APPROVED).count()
                article.save()
            except Exception, e:
                logger.exception('update article comment_count failed, exception: %s' % e)
