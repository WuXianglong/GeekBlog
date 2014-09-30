# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.http import urlencode

from geekblog.ueditor.commands import *
from geekblog.ueditor import settings as u_settings


def calc_path(output_path, instance=None):
    """
    修正输入的文件路径,输入路径的标准格式：abc,不需要前后置的路径符号
    如果输入的路径参数是一个函数则执行，否则可以拉接受时间格式化，
    用来生成如file20121208.bmp的重命名格式
    """
    if callable(output_path):
        try:
            output_path = output_path(instance)
        except:
            output_path = ""
    else:
        try:
            import datetime
            output_path = datetime.datetime.now().strftime(output_path)
        except:
            pass

    return output_path


class UEditorWidget(forms.Textarea):

    def __init__(self, attrs=None):

        params = attrs.copy()

        width = params.pop("width")
        height = params.pop("height")
        toolbars = params.pop("toolbars", "full")
        image_path = params.pop("image_path", "")
        file_path = params.pop("file_path", "")
        upload_settings = params.pop("upload_settings", {})
        settings = params.pop("settings", {})
        command = params.pop("command", None)
        event_handler = params.pop("event_handler", None)

        # 扩展命令
        self.command = command
        self.event_handler = event_handler
        # 上传路径
        self.upload_settings = upload_settings.copy()
        self.upload_settings.update({
            "imagePathFormat": image_path,
            "filePathFormat": file_path
        })
        # 保存
        self._upload_settings = self.upload_settings.copy()
        self.recalc_path(None)

        self.ueditor_settings = {
            'toolbars': toolbars,
            'initialFrameWidth': width,
            'initialFrameHeight': height,
        }
        # 以下处理工具栏设置，将normal,mini等模式名称转化为工具栏配置值
        try:
            if type(toolbars) == str:
                if toolbars == "full":
                    del self.ueditor_settings['toolbars']
                else:
                    self.ueditor_settings["toolbars"] = u_settings.TOOLBARS_SETTINGS[toolbars]
        except:
            pass
        self.ueditor_settings.update(settings)
        super(UEditorWidget, self).__init__(attrs)

    def recalc_path(self, model_inst):
        """ 计算上传路径,允许是function """
        try:
            tmp_settings = self.upload_settings
            for key in ("filePathFormat", "imagePathFormat", "scrawlPathFormat", "videoPathFormat",
                        "snapscreenPathFormat", "catcherPathFormat", "imageManagerListPath", "fileManagerListPath"):
                if key in self._upload_settings:
                    tmp_settings[key] = calc_path(self._upload_settings[key], model_inst)
            # 设置默认值，未指定涂鸦、截图、远程抓图、图片目录时,默认均等于imagePath
            if tmp_settings['imagePathFormat'] != "":
                for key in ('scrawlPathFormat', 'videoPathFormat', 'snapscreenPathFormat', 'catcherPathFormat', 'imageManagerListPath'):
                    tmp_settings[key] = tmp_settings[key] if key in self._upload_settings else tmp_settings['imagePathFormat']
            if tmp_settings['filePathFormat'] != "":
                tmp_settings['fileManagerListPath'] = tmp_settings['fileManagerListPath'] if "fileManagerListPath" in self._upload_settings else tmp_settings['filePathFormat']
        except:
            pass

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        # 传入模板的参数
        editor_id = "id_%s" % name.replace("-", "_")
        tmp_ueditor_settings = {
            "name": name,
            "id": editor_id,
            "value": value
        }
        if isinstance(self.command, list):
            cmdjs = ""
            for cmd in self.command:
                cmdjs += cmd.render(editor_id)
            tmp_ueditor_settings["commands"] = cmdjs

        tmp_ueditor_settings["settings"] = self.ueditor_settings.copy()
        tmp_ueditor_settings["settings"].update({
            "serverUrl": "/ueditor/controller/?%s" % urlencode(self._upload_settings)
        })
        # 生成事件侦听
        if self.event_handler:
            tmp_ueditor_settings["bindEvents"] = self.event_handler.render(editor_id)

        context = {
            'UEditor': tmp_ueditor_settings,
            'STATIC_URL': settings.STATIC_URL,
            'STATIC_ROOT': settings.STATIC_ROOT,
            'MEDIA_URL': settings.MEDIA_URL,
            'MEDIA_ROOT': settings.MEDIA_ROOT
        }
        return mark_safe(render_to_string('ueditor.html', context))

    class Media:
        css = {
            "all": ("ueditor/themes/default/css/ueditor.min.css", "ueditor/themes/iframe.css")
        }
        js = ("ueditor/ueditor.config.js", "ueditor/ueditor.all.min.js")


class AdminUEditorWidget(AdminTextareaWidget, UEditorWidget):

    def __init__(self, **kwargs):
        super(AdminUEditorWidget, self).__init__(**kwargs)
