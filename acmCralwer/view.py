# coding=utf-8
__author__ = 'exbot'
import tornado.web
import tornado.gen
import tornado.httpclient
import datetime
import urllib2

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
    #@tornado.gen.engine
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        mainName = self.get_argument("mainName")
        viceName = self.get_argument("viceName", None)
        if self.isNameValid(mainName):
            import cralwer
            import json
            query = cralwer.crawler(queryName=mainName)
            client = tornado.httpclient.AsyncHTTPClient()
            # non-block part
            cnt = 0
            for oj,website,acRegex,submitRegex in query.getNoAuthRules():
                # non-block for each OJ
                cnt +=1
                url = website %mainName
                req = tornado.httpclient.HTTPRequest(url,headers=query.headers,request_timeout=5)
                response =  yield tornado.gen.Task(client.fetch,req)
                if response.code == 200:
                    query.actRegexRules(response.body,acRegex,submitRegex,oj)
                else:
                    pass

            # uestc
            acdreamURL = 'http://acm.uestc.edu.cn/user/userCenterData/%s' %mainName
            response = yield tornado.gen.Task(client.fetch,acdreamURL,headers=query.headers)
            if response.code == 200:
                query.getAsyncUestc(response.body)
                print 'uestc',datetime.datetime.now()
            else:
                pass

            acdreamURL = 'http://acdream.info/user/%s' % mainName
            response = yield tornado.gen.Task(client.fetch, acdreamURL, headers=query.headers)
            if response.code == 200:
                query.getAsyncACdream(response.body)
                print 'acdream',datetime.datetime.now()
            else:
                pass

            #codeforces and vjudge blocking part
            query.getcodeforces()
            query.getVjudge()




        else:
            raise tornado.web.HTTPError(500,log_message='Invalid name')
        if viceName and self.isNameValid(viceName):
            query.changeCurrentName(viceName)
            import cralwer
            import json
            query = cralwer.crawler(queryName=viceName)
            client = tornado.httpclient.AsyncHTTPClient()
            # non-block part
            cnt = 0
            for oj, website, acRegex, submitRegex in query.getNoAuthRules():
                # non-block for each OJ
                cnt += 1
                url = website % viceName
                # make up task
                req = tornado.httpclient.HTTPRequest(url, headers=query.headers, request_timeout=5)
                response = yield tornado.gen.Task(client.fetch, req)
                if response.code == 200:
                    query.actRegexRules(response.body, acRegex, submitRegex, oj)
                else:
                    pass

            # uestc
            acdreamURL = 'http://acm.uestc.edu.cn/user/userCenterData/%s' % viceName
            response = yield tornado.gen.Task(client.fetch, acdreamURL, headers=query.headers)
            if response.code == 200:
                query.getAsyncUestc(response.body)
                print 'uestc', datetime.datetime.now()
            else:
                pass

            acdreamURL = 'http://acdream.info/user/%s' % viceName
            response = yield tornado.gen.Task(client.fetch, acdreamURL, headers=query.headers)
            if response.code == 200:
                query.getAsyncACdream(response.body)
                print 'acdream', datetime.datetime.now()
            else:
                pass

            # codeforces and vjudge blocking part
            query.getcodeforces()
            query.getVjudge()
        else:
            pass
        # prepare the json
        dataDict = {}
        # dataDict['ac'] = query.acArchive
        dataDict['ac'] = {}
        for key, value in query.acArchive.items():
            dataDict['ac'][key] = list(value)
        dataDict['submit'] = query.submitNum
        dataDict['wrongOJ'] = query.wrongOJ
        self.write(json.dumps(dataDict))
        self.finish()


    def isNameValid(self, queryName):
        '''
        just a regex function to detect whether queryName is correct.
        :param queryName: name that waiting for detect
        :return: boolean value whether name is valid or not.
        '''
        import re
        return re.match(r'^\w*$', queryName)


