# -*- coding: utf-8 -*-
import random
import datetime

SIZE_UNIT = {"Byte": 1, "KB": 1024, "MB": 1048576, "GB": 1073741824, "TB": 1099511627776L}


def fix_file_path(output_path, instance=None):
    """ 修正输入的文件路径,输入路径的标准格式：abc,不需要前后置的路径符号 """
    if callable(output_path):
        try:
            output_path = output_path(instance)
        except:
            output_path = ""
    else:
        try:
            output_path = datetime.datetime.now().strftime(output_path)
        except:
            pass
        if len(output_path) > 0:
            output_path = "%s/" % output_path.strip("/")

    return output_path


def generate_random_filename(filename):
    """ 在上传的文件名后面追加一个日期时间+随机, 如abc.jpg --> abc_20120801202409.jpg """
    from os.path import splitext
    f_name, f_ext = splitext(filename)

    return "%s_%s%s%s" % (f_name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S_"), \
            random.randrange(10, 99), f_ext)


class FileSize():
    """ 文件大小类 """

    def __init__(self, size):
        self.size = long(FileSize.format_size(size))

    @staticmethod
    def format_size(size):
        import re
        if isinstance(size, int) or isinstance(size, long):
            return size

        if isinstance(size, str):
            o_size = size.lstrip().upper().replace(" ", "")
            pattern = re.compile(r"(\d*\.?(?=\d)\d*)(byte|kb|mb|gb|tb)", re.I)
            match = pattern.match(o_size)
            if match:
                m_size, m_unit = match.groups()
                m_size = long(m_size) if m_size.find(".") == -1 else float(m_size)
                return m_size * SIZE_UNIT[m_unit] if m_unit != "BYTE" else m_size
        return 0

    @property
    def size(self):
        """ 返回字节为单位的值 """
        return self.size

    @size.setter
    def size(self, new_size):
        try:
            self.size = long(new_size)
        except:
            self.size = 0

    @property
    def friend_value(self):
        """ 返回带单位的自动值 """
        if self.size < SIZE_UNIT["KB"]:
            unit = "Byte"
        elif self.size < SIZE_UNIT["MB"]:
            unit = "KB"
        elif self.size < SIZE_UNIT["GB"]:
            unit = "MB"
        elif self.size < SIZE_UNIT["TB"]:
            unit = "GB"
        else:
            unit = "TB"

        if (self.size % SIZE_UNIT[unit]) == 0:
            return "%s%s" % ((self.size / SIZE_UNIT[unit]), unit)
        else:
            return "%0.2f%s" % (round(float(self.size) / float(SIZE_UNIT[unit]), 2), unit)

    def __str__(self):
        return self.friend_value

    def __add__(self, other):
        if not isinstance(other, FileSize):
            other = FileSize(other)
        return FileSize(other.size + self.size)

    def __sub__(self, other):
        if not isinstance(other, FileSize):
            other = FileSize(other)
        return FileSize(self.size - other.size)

    def __gt__(self, other):
        if not isinstance(other, FileSize):
            other = FileSize(other)
        return True if self.size > other.size else False

    def __lt__(self, other):
        if not isinstance(other, FileSize):
            other = FileSize(other)
        return True if other.size > self.size else False

    def __ge__(self, other):
        if not isinstance(other, FileSize):
            other = FileSize(other)
        return True if self.size >= other.size else False

    def __le__(self, other):
        if not isinstance(other, FileSize):
            other = FileSize(other)
        return True if other.size >= self.size else False
