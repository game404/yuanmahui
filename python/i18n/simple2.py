# -*- coding: utf-8 -*-
import os
import gettext

APP_NAME = "sample"
LOCALE_DIR = os.path.abspath("locale")

# 将域APP_NAME与LOCALE_DIR目录绑定，
# 这样gettext函数会在LOCALE_DIR目录下搜索对应语言的二进制APP_NAME.mo文件
gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
# 声明使用现在的域，可以使用多个域，便可以为同一种语言提供多套翻译，
# 本程序只使用了一个域
gettext.textdomain(APP_NAME)

_ = gettext.gettext


if __name__ == "__main__":
    print(_("hello Game_404"))
    print(_("hello python"))
