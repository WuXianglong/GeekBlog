# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
多说API测试文件。作为通用的Python程序，没有使用Django的TestCase
"""
import os
import unittest
try:
    import json
    _parse_json = lambda s: json.loads(s)
except ImportError:
    try:
        import simplejson
        _parse_json = lambda s: simplejson.loads(s)
    except ImportError:
        from django.utils import simplejson
        _parse_json = lambda s: simplejson.loads(s)

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import duoshuo

import utils


class DuoshuoAPITest(unittest.TestCase):
    DUOSHUO_SHORT_NAME = 'official'
    DUOSHUO_SECRET = 'a' * 32
    API = duoshuo.DuoshuoAPI(short_name=DUOSHUO_SHORT_NAME, secret=DUOSHUO_SECRET)

    def test_host(self):
        api = self.API
        host = api.host
        self.assertEqual(host, 'api.duoshuo.com')

    def test_get_url(self):
        redirect_uri = 'example.com'
        api = self.API
        url = utils.get_url(api, redirect_uri=redirect_uri)
        self.assertEqual(url,
            'http://%s/oauth2/authorize?client_id=%s&redirect_uri=%s&response_type=code' %
            (api.host, self.DUOSHUO_SHORT_NAME, redirect_uri)
        )

    def test_user_api(self):
        api = self.API
        response = api.users.profile(user_id=1)
        user_id = response['response']['user_id']

        self.assertEqual(int(user_id), 1)

    # 以下测试要是short_name和secret正确设置

    # def test_log_api(self):
    #     api = self.API
    #     response = api.log.list()
    #     code = response['code']
    #     self.assertEqual(int(code), 0)

if __name__ == '__main__':
    unittest.main()
