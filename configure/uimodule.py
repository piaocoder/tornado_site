#coding=utf-8
__author__ = 'exbot'

import setting
import tornado.web

class settingOptionModule(tornado.web.UIModule):
    def render(self,item):
        if hasattr(setting,item):
            return getattr(setting,item)
        else:
            return ''
