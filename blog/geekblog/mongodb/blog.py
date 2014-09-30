#! -*- coding:utf-8 -*-
import logging
from pymongo import DESCENDING
from geekblog.mongodb import MongodbStorage, IncrementalId, set_default_order, cursor_to_list

logger = logging.getLogger('geekblog')

TAG_INFO_FIELDS = {
    '_id': 0,
    'id': 1,
    'name': 1,
    'slug': 1,
    'article_count': 1,
}

LINK_INFO_FIELDS = {
    '_id': 0,
    'id': 1,
    'type': 1,
    'title': 1,
    'icon_url': 1,
    'address': 1,
    'description': 1,
}

SLIDER_INFO_FIELDS = {
    '_id': 0,
    'id': 1,
    'title': 1,
    'image_url': 1,
    'jump_url': 1,
    'description': 1,
}

CATE_BRIEF_INFO_FIELDS = {
    '_id': 0,
    'id': 1,
    'name': 1,
    'slug': 1,
}

CATE_DETAIL_INFO_FIELDS = {
    '_id': 0,
    'id': 1,
    'name': 1,
    'slug': 1,
    'description': 1,
    'icon_url': 1,
    'parent_id': 1,
    'has_child': 1,
    'article_count': 1,
    'views_count': 1,
}

ARTICLE_BRIEF_INFO_FIELDS = {
    '_id': 0,
    'id': 1,
    'title': 1,
    'slug': 1,
}

ARTICLE_DETAIL_INFO_FIELDS = {
    '_id': 0,
    'id': 1,
    'title': 1,
    'slug': 1,
    'category_id': 1,
    'category_name': 1,
    'category_slug': 1,
    'description': 1,
    'content': 1,
    'mark': 1,
    'enable_comment': 1,
    'login_required': 1,
    'views_count': 1,
    'publish_date': 1,
    'thumbnail_url': 1,
    'tags': 1,
}


class BlogMongodbStorage(MongodbStorage):

    db_name = "blog"
    DATE_ORDER = [("publish_date", DESCENDING)]

    def __init__(self, conn_str):
        super(BlogMongodbStorage, self).__init__(conn_str, self.db_name)
        self._ids = IncrementalId(self._db)
        self._db.articles.ensure_index("id")
        self._db.articles.ensure_index("category_id")
        self._db.articles.ensure_index("category_slug")

    def delete_item(self, table, cond):
        eval('self._db.%s.remove(%s)' % (table, cond))

    def upsert_item(self, table, cond, item, upsert=False, multi=False):
        if table == 'articles':
            # if table is articles and item is existed, remove views_count and comment_count
            if eval("self._db.%s.find_one(%s)" % (table, cond)):
                for key in ('views_count', 'comment_count'):
                    if key in item:
                        del item[key]
        # TODO: eval is not good
        eval("self._db.%s.update(%s, {'$set': %s}, upsert=%s, multi=%s)" % (table, cond, item, upsert, multi))

    def get_article_by_id(self, a_id):
        cond = {'id': long(a_id)}
        article_infos = self._db.articles.find_one(cond, fields=ARTICLE_DETAIL_INFO_FIELDS)
        return article_infos

    def get_article_by_slug(self, slug):
        cond = {'slug': slug}
        article_infos = self._db.articles.find_one(cond, fields=ARTICLE_DETAIL_INFO_FIELDS)
        return article_infos

    def get_prev_article(self, publish_date):
        cond = {'publish_date': {'$lt': publish_date}}
        article_infos = self._db.articles.find_one(cond, sort=[('publish_date', self.ORDER_DESC)], fields=ARTICLE_BRIEF_INFO_FIELDS)
        return article_infos

    def get_next_article(self, publish_date):
        cond = {'publish_date': {'$gt': publish_date}}
        article_infos = self._db.articles.find_one(cond, sort=[('publish_date', self.ORDER_ASC)], fields=ARTICLE_BRIEF_INFO_FIELDS)
        return article_infos

    def get_tag_info_by_slug(self, tag_slug):
        cond = {'slug': tag_slug}
        tag = self._db.tags.find_one(cond, fields=TAG_INFO_FIELDS)
        return tag

    def get_cate_info_by_slug(self, cate_slug):
        cond = {'slug': cate_slug}
        cate = self._db.categories.find_one(cond, fields=CATE_BRIEF_INFO_FIELDS)
        return cate

    @cursor_to_list
    @set_default_order
    def get_all_links(self, order=None):
        links = self._db.links.find({}, sort=order, fields=LINK_INFO_FIELDS)
        return links

    @cursor_to_list
    @set_default_order
    def get_all_sliders(self, order=None):
        sliders = self._db.sliders.find({}, sort=order, fields=SLIDER_INFO_FIELDS)
        return sliders

    @cursor_to_list
    def get_tags(self):
        # display 20 tags in web pages at most and sort by article count.
        tags = self._db.tags.find({}, sort=[('article_count', self.ORDER_DESC)], fields=TAG_INFO_FIELDS, limit=20)
        return tags

    @cursor_to_list
    @set_default_order
    def query_categories(self, parents=[0], start_index=0, count=20, order=None, with_total=False):
        cond = {'parent_id': {'$in': parents}}
        results = self._db.categories.find(cond, skip=start_index, limit=count, sort=order, fields=CATE_DETAIL_INFO_FIELDS)
        if with_total:
            total = self._db.categories.find(cond).count()
            return {'results': results, 'total': total}
        return results

    @cursor_to_list
    def get_newest_articles(self, count=5, has_login=False):
        cond = {'login_required': False} if not has_login else {}
        article_infos = self._db.articles.find(cond, sort=[('publish_date', self.ORDER_DESC)], skip=0, limit=count, fields=ARTICLE_BRIEF_INFO_FIELDS)
        return article_infos

    @cursor_to_list
    def get_articles(self, cond, start_index=0, count=10, order=None, fields=ARTICLE_DETAIL_INFO_FIELDS, has_login=False, with_total=False):
        if not has_login:    # if no user login, add login_required cond
            cond['login_required'] = False
        results = self._db.articles.find(cond, skip=start_index, limit=count, sort=self.DATE_ORDER, fields=fields)
        if with_total:
            total = self._db.articles.find(cond).count()
            page_count = (total + count - 1) / count
            return {'results': results, 'total': total, 'page_count': page_count}
        return results

    @cursor_to_list
    def get_tag_articles(self, tag_id, start_index=0, count=10, order=None, fields=ARTICLE_DETAIL_INFO_FIELDS, has_login=False, with_total=False):
        cond = {'tag_ids': tag_id}
        results = self.get_articles(cond, start_index=start_index, count=count, order=order, fields=fields, has_login=has_login, with_total=with_total)
        return results

    @cursor_to_list
    def get_cate_articles(self, cate_id, start_index=0, count=10, order=None, fields=ARTICLE_DETAIL_INFO_FIELDS, has_login=False, with_total=False):
        cond = {'$or': [{'category_id': cate_id}, {'parent_cate_id': cate_id}]}
        results = self.get_articles(cond, start_index=start_index, count=count, order=order, fields=fields, has_login=has_login, with_total=with_total)
        return results

    @cursor_to_list
    def search_articles(self, keyword, start_index=0, count=10, order=None, fields=ARTICLE_DETAIL_INFO_FIELDS, has_login=False, with_total=False):
        import re
        regx = re.compile(keyword, re.IGNORECASE)
        cond = {'$or': [{'title': {'$regex': regx}}, {'description': {'$regex': regx}}]}
        results = self.get_articles(cond, start_index=start_index, count=count, order=order, fields=fields, has_login=has_login, with_total=with_total)
        return results

    @cursor_to_list
    def get_need_sync_comments(self, start_time):
        return self._db.comments.find({'created_time': {'$gt': start_time}})

    def save_sync_log_id(self, data):
        """ save sync log id when sync comments from duoshuo """
        self._db.log_ids.save(data)

    def get_last_log_id(self):
        log_id = self._db.log_ids.find_one({}, sort=[('sync_time', self.ORDER_DESC)])
        return log_id['log_id'] if log_id else 0

    def increment_article_views_count(self, a_id):
        """ increments the value of article views_count """
        self._db.articles.update({'id': long(a_id)}, {'$inc': {'views_count': 1}})
