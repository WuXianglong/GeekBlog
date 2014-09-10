# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.admin import widgets as admin_widgets

from blogcore.ueditor.widgets import UEditorWidget, AdminUEditorWidget


class UEditorField(models.TextField):
    """
    初始化可选参数:
        initial: 初始内容
        width, height:编辑器的宽度和高度, 以像素为单位
        toolbars: 配置你想显示的工具栏, 取值为mini, normal, full, 代表小, 一般和全部
        image_path: 图片上传的路径, 如"images/", 实现上传到"{{ MEDIA_ROOT }}/images"文件夹
        file_path: 附件上传的路径, 如"files/", 实现上传到"{{ MEDIA_ROOT }}/files"文件夹
    """
    def __init__(self, verbose_name=None, width=600, height=400, toolbars="normal",
            image_path="", file_path="", upload_settings=None, settings=None, command=None, event_handler=None, **kwargs):
        for param in (upload_settings, settings):
            if param is None:
                param = {}
        self.ueditor_settings = locals().copy()
        kwargs["verbose_name"] = verbose_name
        del self.ueditor_settings["self"], self.ueditor_settings["kwargs"], self.ueditor_settings["verbose_name"]
        super(UEditorField, self).__init__(**kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': UEditorWidget(attrs=self.ueditor_settings)}
        defaults.update(kwargs)
        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = AdminUEditorWidget(attrs=self.ueditor_settings)
        return super(UEditorField, self).formfield(**defaults)
