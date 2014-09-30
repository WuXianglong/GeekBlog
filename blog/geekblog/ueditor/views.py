# -*- coding: utf-8 -*-
import os
import json
import urllib
import random
import logging
import datetime

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from geekblog.ueditor import settings as ueditor_settings

logger = logging.getLogger('geekblog')


def get_path_format_vars():
    return {
        "year": datetime.datetime.now().strftime("%Y"),
        "month": datetime.datetime.now().strftime("%m"),
        "day": datetime.datetime.now().strftime("%d"),
        "time": datetime.datetime.now().strftime("%H%M%S"),
        "datetime": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "rnd": random.randrange(100, 999)
    }


def save_upload_file(post_file, file_path):
    """ save upload file """
    try:
        f = open(file_path, 'wb')
        for chunk in post_file.chunks():
            f.write(chunk)
    except Exception, e:
        f.close()
        logger.error("save upload file failed, error: %s" % e)
        return u"写入文件错误: %s" % e.message
    f.close()
    return u"SUCCESS"


@csrf_exempt
def get_ueditor_settings(request):
    return HttpResponse(json.dumps(ueditor_settings.UEDITOR_UPLOAD_SETTINGS, \
            ensure_ascii=False), content_type="application/javascript")


@csrf_exempt
def get_ueditor_controller(request):
    """ 获取ueditor的后端URL地址 """
    action = request.GET.get("action", "")
    reponse_action = {
        "config": get_ueditor_settings,
        "uploadimage": upload_file,
        "uploadscrawl": upload_file,
        "uploadvideo": upload_file,
        "uploadfile": upload_file,
        "catchimage": catcher_remote_image,
        "listimage": list_files,
        "listfile": list_files,
    }
    return reponse_action[action](request)


@csrf_exempt
def list_files(request):
    """列出文件"""
    if request.method != "GET":
        return HttpResponse(json.dumps(u"{'state:'ERROR'}"), content_type="application/javascript")
    # 取得动作
    action = request.GET.get("action", "listimage")

    allow_files = {
        "listfile": ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get("fileManagerAllowFiles", []),
        "listimage": ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get("imageManagerAllowFiles", [])
    }
    list_sizes = {
        "listfile": ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get("fileManagerListSize", ""),
        "listimage": ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get("imageManagerListSize", "")
    }
    list_paths = {
        "listfile": ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get("fileManagerListPath", ""),
        "listimage": ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get("imageManagerListPath", "")
    }
    # 取得参数
    list_size = long(request.GET.get("size", list_sizes[action]))
    list_start = long(request.GET.get("start", 0))

    files = []
    root_path = os.path.join(settings.MEDIA_ROOT, list_paths[action]).replace("\\", "/")
    files = get_files(root_path, root_path, allow_files[action])

    if (len(files) == 0):
        return_info = {
            "state": u"未找到匹配文件！",
            "list": [],
            "start": list_start,
            "total": 0
        }
    else:
        return_info = {
            "state": u"SUCCESS",
            "list": files[list_start: list_start + list_size],
            "start": list_start,
            "total": len(files)
        }

    return HttpResponse(json.dumps(return_info), content_type="application/javascript")


def get_files(root_path, cur_path, allow_types=None):
    files = []
    items = os.listdir(cur_path)
    for item in items:
        item = unicode(item)
        item_fullname = os.path.join(root_path, cur_path, item).replace("\\", "/")
        if os.path.isdir(item_fullname):
            files.extend(get_files(root_path, item_fullname, allow_types))
        else:
            ext = os.path.splitext(item_fullname)[1]
            is_allow_list = allow_types is not None and (len(allow_types) == 0) or (ext in allow_types)
            if is_allow_list:
                files.append({
                    "url": urllib.basejoin(settings.MEDIA_URL, \
                            os.path.join(os.path.relpath(cur_path, root_path), item).replace("\\", "/")),
                    "mtime": os.path.getmtime(item_fullname)
                })

    return files


@csrf_exempt
def upload_file(request):
    """ 上传文件 """
    if not request.method == "POST":
        return HttpResponse(json.dumps(u"{'state:'ERROR'}"), content_type="application/javascript")

    state = "SUCCESS"
    action = request.GET.get("action")
    # 上传文件
    upload_field_names = {
        "uploadfile": "fileFieldName",
        "uploadimage": "imageFieldName",
        "uploadscrawl": "scrawlFieldName",
        "catchimage": "catcherFieldName",
        "uploadvideo": "videoFieldName",
    }
    upload_field_name = request.GET.get(upload_field_names[action], \
            ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get(action, "upfile"))

    # 上传涂鸦，涂鸦是采用base64编码上传的，需要单独处理
    if action == "uploadscrawl":
        upload_file_name = "scrawl.png"
        upload_file_size = 0
    else:
        # 取得上传的文件
        file = request.FILES.get(upload_field_name, None)
        if file is None:
            return HttpResponse(json.dumps(u"{'state:'ERROR'}"), content_type="application/javascript")
        upload_file_name = file.name
        upload_file_size = file.size

    # 取得上传的文件的原始名称
    upload_original_name, upload_original_ext = os.path.splitext(upload_file_name)

    # 文件类型检验
    upload_allow_types = {
        "uploadfile": "fileAllowFiles",
        "uploadimage": "imageAllowFiles",
        "uploadvideo": "videoAllowFiles",
    }
    if action in upload_allow_types:
        allow_type = list(request.GET.get(upload_allow_types[action], \
                ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get(upload_allow_types[action], "")))
        if not upload_original_ext in allow_type:
            state = u"服务器不允许上传%s类型的文件。" % upload_original_ext

    # 大小检验
    upload_max_sizes = {
        "uploadfile": "filwMaxSize",
        "uploadimage": "imageMaxSize",
        "uploadscrawl": "scrawlMaxSize",
        "uploadvideo": "videoMaxSize",
    }
    max_size = long(request.GET.get(upload_max_sizes[action], \
            ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get(upload_max_sizes[action], 0)))
    if max_size != 0:
        from geekblog.ueditor.utils import FileSize
        max_file_size = FileSize(max_size)
        if upload_file_size > max_file_size.size:
            state = u"上传文件大小不允许超过%s。" % max_file_size.friend_value

    # 检测保存路径是否存在,如果不存在则需要创建
    upload_path_formats = {
        "uploadfile": "filePathFormat",
        "uploadimage": "imagePathFormat",
        "uploadscrawl": "scrawlPathFormat",
        "uploadvideo": "videoPathFormat",
    }

    path_format_var = get_path_format_vars()
    path_format_var.update({
        "basename": upload_original_name,
        "extname": upload_original_ext[1:],
        "filename": upload_file_name,
    })
    # 取得输出文件的路径
    output_path_format, output_path, output_file = get_output_path(request, \
            upload_path_formats[action], path_format_var)

    # 所有检测完成后写入文件
    if state == "SUCCESS":
        if action == "uploadscrawl":
            state = save_scrawl_file(request, os.path.join(output_path, output_file))
        else:
            # 保存到文件中，如果保存错误，需要返回ERROR
            state = save_upload_file(file, os.path.join(output_path, output_file))

    # 返回数据
    return_info = {
        'url': urllib.basejoin(settings.MEDIA_URL, output_path_format),    # 保存后的文件名称
        'original': upload_file_name,    # 原始文件名
        'type': upload_original_ext,
        'state': state,    # 上传状态，成功时返回SUCCESS,其他任何值将原样返回至图片上传框中
        'size': upload_file_size
    }
    return HttpResponse(json.dumps(return_info, ensure_ascii=False), content_type="application/javascript")


@csrf_exempt
def catcher_remote_image(request):
    """
        远程抓图，当catchRemoteImageEnable:true时，
        如果前端插入图片地址与当前web不在同一个域，则由本函数从远程下载图片到本地
    """
    if not request.method == "POST":
        return HttpResponse(json.dumps(u"{'state:'ERROR'}"), content_type="application/javascript")

    state = "SUCCESS"
    allow_type = list(request.GET.get("catcherAllowFiles", \
            ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get("catcherAllowFiles", "")))
    max_size = long(request.GET.get("catcherMaxSize", \
            ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get("catcherMaxSize", 0)))

    catcher_infos = []
    path_format_var = get_path_format_vars()
    remote_urls = request.POST.getlist("source[]", [])

    for remote_url in remote_urls:
        # 取得上传的文件的原始名称
        remote_file_name = os.path.basename(remote_url)
        remote_original_name, remote_original_ext = os.path.splitext(remote_file_name)
        # 文件类型检验
        if remote_original_ext in allow_type:
            path_format_var.update({
                "basename": remote_original_name,
                "extname": remote_original_ext[1:],
                "filename": remote_original_name
            })
            # 计算保存的文件名
            o_path_format, o_path, o_file = get_output_path(request, "catcherPathFormat", path_format_var)
            o_filename = os.path.join(o_path, o_file).replace("\\", "/")
            # 读取远程图片文件
            try:
                remote_image = urllib.urlopen(remote_url)
                # 将抓取到的文件写入文件
                try:
                    f = open(o_filename, 'wb')
                    f.write(remote_image.read())
                    f.close()
                    state = "SUCCESS"
                except Exception, e:
                    state = u"写入抓取图片文件错误: %s" % e.message
            except Exception, e:
                state = u"抓取图片错误： %s" % e.message

            catcher_infos.append({
                "state": state,
                "url": urllib.basejoin(settings.MEDIA_URL, o_path_format),
                "size": os.path.getsize(o_filename),
                "title": os.path.basename(o_file),
                "original": remote_file_name,
                "source": remote_url
            })

    return_info = {
        "state": "SUCCESS" if len(catcher_infos) > 0 else "ERROR",
        "list": catcher_infos
    }

    return HttpResponse(json.dumps(return_info, ensure_ascii=False), content_type="application/javascript")


def get_output_path(request, path_format, path_format_var):
    # 取得输出文件的路径
    output_path_format = (request.GET.get(path_format, \
            ueditor_settings.UEDITOR_SETTINGS["defaultPathFormat"]) % path_format_var).replace("\\", "/")
    # 分解output_path_format
    output_path, output_file = os.path.split(output_path_format)
    output_path = os.path.join(settings.MEDIA_ROOT, output_path)
    if not output_file:    # 如果output_file为空说明传入的output_path_format没有包含文件名，因此需要用默认的文件名
        output_file = ueditor_settings.UEDITOR_SETTINGS["defaultPathFormat"] % path_format_var
        output_path_format = os.path.join(output_path_format, output_file)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return (output_path_format, output_path, output_file)


@csrf_exempt
def save_scrawl_file(request, filename):
    """ 涂鸦功能上传处理 """
    import base64
    try:
        content = request.POST.get(ueditor_settings.UEDITOR_UPLOAD_SETTINGS.get("scrawlFieldName", \
                "upfile"))
        f = open(filename, 'wb')
        f.write(base64.decodestring(content))
        f.close()
        state = "SUCCESS"
    except Exception, e:
        state = "写入图片文件错误: %s" % e.message
    return state
