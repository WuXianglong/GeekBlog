========
GeekBlog
========

GeekBlog is a blog system based on django and python.

初始化website的步骤
===================

根据install_deps.sh安装所有依赖
-------------------------------

    1). cd GeekBlog/core/scripts && sudo ./install_deps.sh
    2). cd GeekBlog/blog/scripts && sudo ./install_deps.sh

创建存放静态文件的目录
----------------------

    1). 默认目录是: /mnt/blog/upload/(images|files)
    2). cd /mnt && sudo mkdir blog && sudo chmod 777 blog
    3). cd blog && sudo mkdir upload && sudo chmod 777 upload
    4). cd upload && sudo mkdir images files && sudo chmod 777 files images

创建数据库
----------

    1). create database geekblog character set utf8;
    2). grant all on geekblog.* to 'username'@'localhost' identified by 'password';

初始化数据库
------------

    1). cd GeekBlog/blog/geekblog
    2). 运行python manage.py syncdb, 输入初始化的用户和密码

生成翻译文件
------------

    1). django-admin.py makemessages -a
    2). django-admin.py makemessages -d djangojs -a
    3). django-admin.py compilemessages --locale=zh_CN
    4). https://github.com/django-mptt/django-mptt/commit/4b6a9758396450651bc2d02b2c7d49bac6cd3f25

运行website
-----------

    1). cd GeekBlog/blog/geekblog
    2). 运行python manage.py runserver 0.0.0.0:8080
    3). 打开浏览器, 访问localhost:8080/console即可看到控制台界面
