#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import Image
import ImageDraw
import ImageFont
import random
import StringIO
from math import ceil
from django.http import HttpResponse

_DEFAULT_SESSION_KEY = 'django-verify-code'
_ENABLED_STRINGS = '0123456789abcdefghijklmnopqrstuvwxyz'
_DEFAULT_FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DejaVuSans.ttf")


class VerifyCode(object):

    def __init__(self, request, c_type='operation', img_width=150, img_height=30, font_path=None, session_key=None):
        """ 初始化对象信息. """
        self.django_request = request

        # 验证码类型：运算(operation), 字符串(string)
        self.code_type = c_type
        self.img_width = img_width
        self.img_height = img_height
        # 验证码字体颜色
        self.font_color = ["black", "darkblue", "darkred"]
        self.font_path = font_path or _DEFAULT_FONT_PATH
        self.session_key = session_key or _DEFAULT_SESSION_KEY

    def _generate_operation(self, max_value=50):
        """ 生成运算表达式验证码

        @max_value: 运算式中允许出现的最大数字, 默认为50
        """
        operators = ['-', '+']
        operand_x = random.randrange(1, max_value)
        operand_y = random.randrange(1, max_value)
        if operand_x < operand_y:
            operand_x, operand_y = operand_y, operand_x

        r = random.randrange(0, 2)
        code = "%s %s %s = ?" % (operand_x, operators[r], operand_y)
        result = eval("%s%s%s" % (operand_x, operators[r], operand_y))
        return code, result

    def _generate_string(self, length=4):
        """ 生成字符串验证码

        @length: 字符串验证码允许的长度, 默认为4
        """
        random_chars = [_ENABLED_STRINGS[random.randrange(0, len(_ENABLED_STRINGS))] for i in range(length)]
        code = ''.join(random_chars)
        return code, code

    def _generate_verify_code(self):
        """ 生成验证码和答案 """
        generate_fun = getattr(self, '_generate_%s' % self.code_type, None)
        code, result = generate_fun() if callable(generate_fun) else self._generate_operation()
        self._set_session_value(result)

        return code

    def _set_session_value(self, value):
        """ 将验证码答案放在request session中 """
        self.django_request.session[self.session_key] = str(value)

    def _get_font_size(self):
        """ 将图片高度的80%作为字体大小 """
        s1 = int(self.img_height * 0.8)
        s2 = int(self.img_width / len(self.code))
        return int(min((s1, s2)) + max((s1, s2)) * 0.05)

    def display(self):
        """ 生成并返回验证码图片 """

        # 图片背景颜色
        self.img_background = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
        # 生成图片
        im = Image.new('RGB', (self.img_width, self.img_height), self.img_background)

        # 得到验证码
        self.code = self._generate_verify_code()
        # 调整验证码字符大小
        self.font_size = self._get_font_size()
        # 创建画笔
        draw = ImageDraw.Draw(im)
        # 画随机干扰线,字数越少,干扰线越多
        line_num = 4

        for i in range(random.randrange(line_num - 2, line_num)):
            line_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            xy = (
                random.randrange(0, int(self.img_width * 0.2)),
                random.randrange(0, self.img_height),
                random.randrange(3 * self.img_width / 4, self.img_width),
                random.randrange(0, self.img_height)
            )
            draw.line(xy, fill=line_color, width=int(self.font_size * 0.1))

        # 写验证码
        j = int(self.font_size * 0.3)
        k = int(self.font_size * 0.5)
        x = random.randrange(j, k)    # 起始位置
        for i in self.code:
            # 上下抖动量,字数越多,上下抖动越大
            m = int(len(self.code))
            y = random.randrange(1, 3)

            if i in ('+', '=', '?'):
                # 对计算符号等特殊字符放大处理
                m = ceil(self.font_size * 0.8)
            else:
                # 字体大小变化量,字数越少,字体大小变化越多
                m = random.randrange(0, int(45 / self.font_size) + int(self.font_size / 5))

            self.font = ImageFont.truetype(self.font_path.replace('\\', '/'), self.font_size + int(ceil(m)))
            draw.text((x, y), i, font=self.font, fill=random.choice(self.font_color))
            x += self.font_size * 0.9

        del x
        del draw
        buf = StringIO.StringIO()
        im.save(buf, 'gif')
        buf.closed
        return HttpResponse(buf.getvalue(), 'image/gif')

    def check(self, code):
        """ 检查用户输入的验证码是否正确 """
        _code = self.django_request.session.get(self.session_key) or ''
        if not _code:
            return False
        return _code.lower() == str(code).lower()
