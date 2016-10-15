# coding=utf-8
__author__ = 'exbot'
import tornado.web

class queryHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('queryProblem/index.html',error=False)

    def isNameValid(self,queryName):
        '''
        just a regex function to detect whether queryName is correct.
        :param queryName: name that waiting for detect
        :return: boolean value whether name is valid or not.
        '''
        import re
        return re.match(r'^\w*$',queryName)

    def post(self, *args, **kwargs):
        '''
        just a rendering page
        :param args:
        :param kwargs:
        :return: none
        '''
        mainName = self.get_argument("mainName")
        viceName = self.get_argument("viceName", None)
        # use regex to fill the match the name
        if self.isNameValid(mainName):
            # this name is valid...
            self.render('queryProblem/query.html')
        else:
            self.render('queryProblem/error.html',error=True)