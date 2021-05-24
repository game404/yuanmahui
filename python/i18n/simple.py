# -*- coding: utf-8 -*-
import os
import gettext

APP_NAME = "sample"
LOCALE_DIR = os.path.abspath("locale")

# 这条语句会将_()函数自动放到python的内置命名空间中
gettext.install(APP_NAME, LOCALE_DIR)
# 获取简体中文翻译类的实例
lang_zh_CN = gettext.translation(APP_NAME, LOCALE_DIR, languages=["zh_CN"])
# 获取英文翻译类的实例
lang_en = gettext.translation(APP_NAME, LOCALE_DIR, languages=["en"])


def _(message): return message


if __name__ == "__main__":
    # 安装中文
    lang_zh_CN.install()
    print(lang_zh_CN.gettext('hello Game_404'))
    del _
    _ = gettext.gettext
    print(_("hello Game_404"))
    # 安装英文（程序中实时切换回英文）
    lang_en.install()
    print(lang_en.gettext('hello Game_404'))
    print(_("hello python"))
