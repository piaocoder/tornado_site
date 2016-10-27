__author__ = 'kidozh'
# -*- coding: UTF-8 -*-

import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.websocket

class portalHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('portal/index.html')

class aboutHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('portal/about.html')