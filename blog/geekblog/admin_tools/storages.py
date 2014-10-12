# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class LocalFileSystemStorage(FileSystemStorage):

    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.MEDIA_ROOT
        self.location = os.path.abspath(location)
        self.base_url = "http://%s" % settings.SITE_DOMAIN
