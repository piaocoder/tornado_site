# coding=utf-8
__author__ = 'exbot'
import tornado.web
import tornado.gen
class queryIndexHandler(tornado.web.RequestHandler):
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


class queryInfoHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, *args, **kwargs):
        mainName = self.get_argument("mainName")
        viceName = self.get_argument("viceName", None)
        if self.isNameValid(mainName):
            import cralwer
            import json
            query = cralwer.crawler(queryName=mainName)
            # non-block part
            for oj,website,acRegex,submitRegex in query.getNoAuthRules():
                # non-block for each OJ
                yield tornado.gen.Task(query.followRules(oj , website , acRegex , submitRegex))
            # for other oj
            yield tornado.gen.Task(query.getACdream())
            yield tornado.gen.Task(query.getVjudge())
            yield tornado.gen.Task(query.getUestc())
            yield tornado.gen.Task(query.getSpoj())
            yield tornado.gen.Task(query.getcodeforces())
            # prepare the json
            dataDict = {}
            dataDict['ac'] = query.acArchive
            dataDict['submit'] = query.submitNum
            dataDict['wrongOJ'] = query.wrongOJ
            self.finish(json.dumps(dataDict))


        else:
            raise tornado.web.HTTPError(500,log_message='Invalid name')
        if viceName and self.isNameValid(viceName):
            query.changeCurrentName(viceName)


    def isNameValid(self, queryName):
        '''
        just a regex function to detect whether queryName is correct.
        :param queryName: name that waiting for detect
        :return: boolean value whether name is valid or not.
        '''
        import re
        return re.match(r'^\w*$', queryName)


