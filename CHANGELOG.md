ChangeLog
=========

Version 0.9 (2014-01-15)
--------------------------

  * Implete most of geek blog's features, include admin site & blog site.
  * Add django ueditor plugin, which is an open source js rich editor from baidu, version is 1.3.6.
  * Add duoshuo comment plugin.
  * Adjust the css style of admin site and blog site.

Version 1.0 (2014-01-22)
----------------------------

  * Implete archive page and friend link page.
  * Implete login required and enabled comment features.
  * Add icon_url field in Link model to save website favicon icon.
  * Add search box in sidebar and implete search article feature.
  * Add newest comments in side bar.
  * Fix bugs in geekblog project.
  * Fix bugs in duoshuo template tag and implete sync duoshuo comment command.

Version 1.1 (2014-02-13)
----------------------------
  * Fix bugs in ueditor, blog css styles and django ALLOWED_HOSTS settings.
  * Add jQuery ColorBox (A lightweight customizable lightbox plugin for jQuery).

Version 1.2 (2014-07-11)
----------------------------
  * Update UEditor version to 1.4.3.
  * Fix some bugs and remove persional infos from project settings.

Version 1.3 (2014-07-27)
----------------------------
  * Change url defination of article detail page.
  * Update about page and translation files.
  * Fix bugs in project(permission of files & syntax highlighter plugin).


TODOs
=====

  * 控制台新增/修改内容保存之后不能第一次显示出来
  * 控制台order字段修改问题
  * 可配置博客主题
  * 可动态添加Django APP作为插件使用
  * 添加手机访问时的适配页面(利用一些比较成熟的适配框架)
  * 扫一扫即可阅读功能(需要实手机展示页面)
