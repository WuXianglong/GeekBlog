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

Version 1.3.1 (2014-08-03)
----------------------------
  * Update django version from 1.5.2 to 1.6.5 to fix save model bugs.
  * Fix bug when change order of articles.
  * Fix some bugs after updating the version of django.

Version 1.3.2 (2014-08-11)
----------------------------
  * Compress image size.
  * Compress and merge JS & CSS files.

Version 1.3.3 (2014-08-12)
----------------------------
  * Add sitemap url using django sitemap.
  * Use django memcached to cache blog pages and files.
  * Use django-pipeline to merge and compress js and css files.


TODOs
=====

  * 使用djang-pipeline & memcached优化博客(https://github.com/tualatrix/imtx)
  * 增加预览页面
  * 修改object history页面
