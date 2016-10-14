# coding=utf-8
__author__ = 'exbot'
import tornado.web

class queryHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('queryProblem/index.html',error=False)

    def post(self, *args, **kwargs):
        mainName = self.get_argument("mainName")
        viceName = self.get_argument("viceName", None)

        self.render('queryProblem/query.html')