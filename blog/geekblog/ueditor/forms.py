# -*- coding: utf-8 -*-
from django import forms

from ueditor.widgets import UEditorWidget
from ueditor.models import UEditorField as ModelUEditorField


class UEditorField(forms.CharField):

    def __init__(self, label, width=600, height=400, toolbars="full", image_path="", file_path="",
            upload_settings=None, settings=None, command=None, event_handler=None, *args, **kwargs):
        for param in (upload_settings, settings):
            if param is None:
                param = {}
        ueditor_settings = locals().copy()
        del ueditor_settings["self"], ueditor_settings["label"], ueditor_settings["args"], ueditor_settings["kwargs"]
        kwargs["widget"] = UEditorWidget(attrs=ueditor_settings)
        kwargs["label"] = label
        super(UEditorField, self).__init__(*args, **kwargs)


def update_upload_path(model_form, model_inst=None):
    """ 遍历model字段，如果是UEditorField则需要重新计算路径 """
    if model_inst is not None:
        try:
            for field in model_inst._meta.fields:
                if isinstance(field, ModelUEditorField):
                    model_form.__getitem__(field.name).field.widget.recalc_path(model_inst)
        except:
            pass


class UEditorModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UEditorModelForm, self).__init__(*args, **kwargs)
        try:
            if "instance" in kwargs:
                update_upload_path(self, kwargs["instance"])
            else:
                update_upload_path(self, None)
        except Exception:
            pass
