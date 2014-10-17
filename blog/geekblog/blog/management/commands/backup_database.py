#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    BACK_PATH = '/mnt/blog/backup'
    DATE_FROMAT = '%Y%m%d'

    def backup_mysql():
        # gzip blog_20141017.sql
        file_name = 'blog_%s.sql' % datetime.datetime.now().strftime(DATE_FROMAT)

        dump_shell = 'mysqldump -u%s -p%s --add-drop-table --routines %s > '
        gzip_shell = 'gzip '

        subprocess.call(dump_shell, shell=True)
        subprocess.call(gzip_shell, shell=True)

    def backup_mongodb():
        file_name = 'blog_%s.tar.gz' % datetime.datetime.now().strftime(DATE_FROMAT)

        # tar cvf blog.tar.gz blog/
        # sudo rm -rf blog/
        dump_shell = 'mongodump -d blog -o /mnt/blog/backup'
        gzip_shell = 'gzip blog/*'

        subprocess.call(dump_shell, shell=True)
        subprocess.call(gzip_shell, shell=True)
        subprocess.call('sudo rm blog/*', shell=True)

    def upload_to_baidu(file_name, file_path):
        """
        return:
            {
            　    "path" : "/apps/album/1.jpg",
            　    "size" : 372121,
            　    "ctime" : 1234567890,
            　    "mtime" : 1234567890,
            　    "md5" : "cb123afcc12453543ef",
            　    "fs_id" : 12345,
                　"request_id":4043312669
            }
        """
        params = {
            'method': 'upload',
            'path': settings.BAIDU_UPLOAD_PREFIX % file_name,
            'ondup': 'newcopy',    # overwrite or newcopy
            'access_token': '',    # TODO
        }
        return

    def handle(self, server='baidu', **options):
        print 'backup mysql and mongodb data'

        # backup mysql and mongodb
        mysql_file_name, mysql_file_path = self.backup_mysql()
        mongo_file_name, mongo_file_path = self.backup_mongodb()

        # TODO: other servers: dropbox, dbank etc.
        # upload_func = getattr(self, 'upload_to_%s' % server, None)
        # if callable(upload_func):
        #     print 'upload backup files to %s' % server
        #     upload_func(mysql_file_name, mysql_file_path)
        #     upload_func(mongo_file_name, mongo_file_path)
        # else:
        #     print 'invaild server name: %s' % server

