#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import time
import datetime

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from mongodb.blog import BlogMongodbStorage
from mongodb import timestamp2datetime
from blog.models.constants import COMMENT_STATUS

blog_db = BlogMongodbStorage(settings.MONGODB_CONF)
img_regex = re.compile(r'(<img src="[^"]+" alt="[^"]+" title="([^"]+)" class="ds-smiley" />)')


def _clean_content(content):
    all_matches = img_regex.findall(content)

    for item in all_matches:
        content = content.replace(item[0], item[1])

    return content


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
    if meta and isinstance(meta, dict):
        from blog.models import Article, Comment
        a_id = meta.get('thread_key')
        try:
            if action == 'create':
                try:
                    article = Article.objects.get(id=int(a_id))
                except (Article.DoesNotExist, TypeError, ValueError) as e:
                    print 'Article does not exist, ID: %s, error: %s' % (a_id, e)
                    return
                c = Comment()
                c.article = article
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
                c.content = _clean_content(meta.get('message', ''))
                c.author_agent = ''
                status = meta.get('status', '')
                c.status = COMMENT_STATUS.APPROVED if status == 'approved' else (COMMENT_STATUS.NOT_REVIEWED if status == 'pending' else COMMENT_STATUS.REJECTED)
                c.sync_status = 0
                c.save()
                print 'Create comment, article ID: %s, comment ID: %s' % (a_id, c.id)
            elif action == 'approve':
                Comment.objects.filter(duoshuo_id__in=meta).update(status=COMMENT_STATUS.APPROVED)
            elif action == 'spam':
                Comment.objects.filter(duoshuo_id__in=meta).update(status=COMMENT_STATUS.REJECTED)
            elif action in ('delete', 'delete-forever'):
                Comment.objects.filter(duoshuo_id__in=meta).update(hided=True, status=COMMENT_STATUS.REJECTED)
        except Exception, e:
            print 'update article comment failed, exception: %s, comment: %s' % (e, comment)


class Command(BaseCommand):

    def handle(self, action='all', **options):
        print 'sync comment, views_count and comment_count'
        from blog.models import Article

        # sync views_count from mongodb
        articles = blog_db.get_articles({}, count=10000, fields={'_id': 0, 'id': 1, 'views_count': 1}, has_login=True)
        for article in articles:
            print 'update views_count, article ID: %s, views count: %s' % (article['id'], article['views_count'])
            try:
                Article.objects.filter(id=article['id']).update(views_count=article['views_count'])
            except Exception, e:
                print 'sync article views_count failed, exception: %s' % e

        # sync article comments from duoshuo
        # API example: http://dev.duoshuo.com/docs/50037b11b66af78d0c000009
        try:
            api_params = {
                'short_name': getattr(settings, 'DUOSHUO_SHORT_NAME', ''),
                'secret': getattr(settings, 'DUOSHUO_SECRET', ''),
                'since_id': blog_db.get_last_log_id(),
                'limit': 200,
            }
            print 'DUOSHUO api params: %s' % api_params
            while True:
                r = requests.get('http://api.duoshuo.com/log/list.json', params=api_params)
                ret_msg = r.json()
                # if return error or return data length is 0, break
                if ret_msg['code'] != 0 or 'response' not in ret_msg or not bool(ret_msg['response']):
                    break
                response = ret_msg['response']
                for i, comment in enumerate(response):
                    # update since_id for while loop
                    if i == len(response) - 1:
                        api_params['since_id'] = comment['log_id']
                    # update or insert comment
                    _upsert_comment(comment)
            # save sync log_id
            blog_db.save_sync_log_id({'log_id': api_params['since_id'], 'sync_time': int(time.time())})
        except Exception, e:
            print 'sync article comment from duoshuo failed, exception: %s' % e

        # update article comment count
        for article in Article.objects.all().filter(hided=False):
            try:
                article.comment_count = article.comments.all().filter(hided=False, status=COMMENT_STATUS.APPROVED).count()
                article.save()
            except Exception, e:
                print 'update article comment_count failed, exception: %s' % e
