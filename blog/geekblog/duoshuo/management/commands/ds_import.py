# -*- coding: utf-8 -*-
import ast
import json
import urllib
import urllib2
import duoshuo
from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.db.models.loading import get_model
from django.forms.models import model_to_dict

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

DUOSHUO_SHORT_NAME = getattr(settings, "DUOSHUO_SHORTNAME", None)
DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not args:
            raise CommandError('Tell me what\'s data you want synchronization (user/thread/comment)')
        if not DUOSHUO_SHORT_NAME or not DUOSHUO_SECRET:
            raise CommandError('Before you can sync you need to set DUOSHUO_SHORT_NAME and DUOSHUO_SECRET')
        else:
            api = duoshuo.DuoshuoAPI(short_name=DUOSHUO_SHORT_NAME, secret=DUOSHUO_SECRET)
            data = {
                'secret': DUOSHUO_SECRET,
                'short_name': DUOSHUO_SHORT_NAME,
            }
        if args[0] == 'user':
            api_url = '%s://%s.duoshuo.com/api/users/import.json' % (api.uri_schema, DUOSHUO_SHORT_NAME)
            users = User.objects.all()
            users_data = {}
            for user in users:
                avatar = user.get_profile().avatar and user.get_profile().avatar or ''

                data['users[%s][user_key]'% user.id] = user.id
                data['users[%s][name]'% user.id] = user.username
                data['users[%s][email]'% user.id] = user.email
                data['users[%s][avatar]'% user.id] = avatar

            data = urllib.urlencode(data)
            response = urllib2.urlopen(api_url, data).read()

            print '%d %s is success import to Duoshuo' % (len(users), len(users) > 1 and 'users' or 'user')

        elif args[0] == 'comment':
            # api_url = '%s://%s.duoshuo.com/api/posts/import.json' , (api.uri_schema, DUOSHUO_SHORT_NAME)

            # try:
            #     threads = ast.literal_eval(open('duoshuo/threads.json', 'r').read())
            # except IOError:
            #     threads = ''

            # comments = Comment.objects.all()
            # for comment in comments:
            #     data['posts[%s][post_key]'% comment.id] = comment.id
            #     data['posts[%s][author_key]'% comment.id] = comment.user_id
            #     data['posts[%s][author_name]'% comment.id] = comment.user_name
            #     data['posts[%s][author_email]'% comment.id] = comment.user_email
            #     data['posts[%s][created_at]'% comment.id] = comment.user_email
            #     data['posts[%s][message]'% comment.id] = comment.comment
            #     data['posts[%s][flags]'% comment.id] = 'import'
            #     try:
            #         threads['%s_%s_%s' % (comment.content_type.app_label,comment.content_type.model,comment.content_object.id)]
            #     except:
            #         pass
            #     else:
            #         data['posts[%s][thread_id]'% comment.id] = thread_id

            # print '%d %s was success sync;' % (len(comments), len(comments) > 1 and 'comments' or 'comment')

            raise CommandError('Sorry, now just import user')

        elif args[0] == 'thread':
            # api_url = '%s://%s.duoshuo.com/api/threads/import.json' % (api.uri_schema, DUOSHUO_SHORT_NAME)

            # current_site = Site.objects.get_current()
            # if current_site.domain == 'example.com':
            #     raise CommandError('I need to know your domain name, it should not be example.com')
            # else:
            #     print "\033[0;32;40mAll threads will be import to %s, use Ctrl-D/Ctrl+C to break if this domain name is not correct.\033[0m" % current_site.domain

            # _s = raw_input('Please input the thread model name such as `threads.thread`:')
            # if len(_s.split('.')) != 2:
            #     raise CommandError('Model name is invalid.')
            # else:
            #     print "\033[0;32;40mStart  import thread from %s:\033[0m" % _s
            #     app_label, model_name = [s.lower() for s in _s.split('.')]

            # thread_model = get_model(app_label, model_name)
            # if not thread_model:
            #     raise CommandError('Cant\'t find model: %s.' % _s)

            # try:
            #     thread_model.get_absolute_url
            # except AttributeError:
            #     raise CommandError('Please define a get_absolute_url() method.')

            # thread_schema = {'title': '', 'content': ''}
            # thread_schema['title'] = raw_input('Enter thread title filed name: ')
            # thread_schema['content'] = raw_input('Enter thread content filed name: ')

            # threads = thread_model.objects.all()
            # for thread in threads:
            #     data['threads[%s][thread_key]'% thread.id] = '%s_%s_%s' % (app_label, model_name, str(thread.id))
            #     data['threads[%s][url]'% thread.id] = 'http://%s%s' % (current_site.domain, thread.get_absolute_url())
            #     try:
            #         data['threads[%s][title]'% thread.id] = thread.__getattribute__(thread_schema['title'])
            #     except:
            #         pass

            #     try:
            #         data['threads[%s][content]'% thread.id] = thread.__getattribute__(thread_schema['content'])
            #     except:
            #         pass

            # data = urllib.urlencode(data)
            # response = json.loads(urllib2.urlopen(api_url, data).read())

            # _f = open('duoshuo/threads.json', 'w')
            # _f.write(unicode(response['response']))
            # _f.close()

            # print '%d %s was success sync;' % (len(threads), len(threads) > 1 and 'threads' or 'thread')

            raise CommandError('Sorry, now just import user')

        else:
            raise CommandError('Tell me what\'s data you want synchronization (user/thread/comment)')

    # def _comment_to_threads(self, comment):
    #     thread = comment.
