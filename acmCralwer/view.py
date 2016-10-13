# coding=utf-8
__author__ = 'exbot'
import tornado.web

class queryHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('queryProblem/index.html')