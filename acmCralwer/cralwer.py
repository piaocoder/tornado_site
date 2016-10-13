# coding=utf-8
__author__ = 'exbot'

import urllib2
import cookielib
import re
import json
import urllib

class crawler:
    '''
    This is the main crawler which contains a dictionary.
    This dictionary's key is the judge name,value is a set that contains each problem that user has ACed.
    As for submit condition , just store the number.
    '''
    name = ''
    acArchive ={}
    submitNum = {}
    # OJ's name : [user,user]
    wrongOJ = {}
    # match dictionary.dict[oj]:[acRegex],[submitRegex]
    matchDict = {}
    supportedOJ = ['poj','hdu','zoj','codeforce','fzu','acdream','bzoj','ural','csu','hust','spoj','sgu','vjudge','bnu','cqu','uestc']
    def __init__(self,queryName=''):
        '''
        This is the initial part which describe the crawler opener.
        '''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        }
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.name = queryName
        '''
        initialize all the data structure
        '''
        for oj in self.supportedOJ:
            # for achive ,use set
            self.submitNum[oj] = 0
            self.acArchive[oj]=set([])
            # for problem , use list
            self.wrongOJ[oj]=[]

        '''
        read the dictionary which guide spider to browser website and how to match information
        '''
        matchDict = {}
        matchDict['poj'] = {}


    def getInfoNoAuth(self,queryName='kidozh'):
        '''
        This function only browser the website without authentication and also use regex.
        For 'poj','hdu','zoj','fzu','acdream','bzoj','ural','csu','hust','spoj','sgu','vjudge','bnu','cqu','uestc'
        :param query: queryName
        :return:
        '''
        import ConfigParser
        import os
        if queryName == '':
            name = self.name
        else:
            name = queryName
        cf = ConfigParser.ConfigParser()
        configFilePath = os.path.join(os.path.dirname(__file__), "regexDict.ini")
        cf.read(configFilePath)
        # travel all the useable site
        for oj in cf.sections():
            website = cf.get(oj,'website')
            acRegex = cf.get(oj,'acRegex')
            submitRegex = cf.get(oj,'submitRegex')
            print website %name
            req = urllib2.Request(
                url=website %name,
                headers=self.headers
            )
            try:
                html = self.opener.open(req).read()
            except:
                self.wrongOJ[oj].append(name)
                continue
            submission = re.findall(submitRegex, html, re.S)
            acProblem = re.findall(acRegex, html, re.S)
            print '# submission : ',submission
            print '# problem : ',acProblem
            # for submit
            try:
                self.submitNum[oj]+=submission[0]
            except:
                self.wrongOJ[oj] = name
                continue
            # for AC merge all the information
            self.acArchive[oj] = self.acArchive[oj] | set(acProblem)
            print submission[0],acProblem
            return submission[0], acProblem


    def getPOJ(self,queryName=''):
        if queryName == '':
            name = self.name
        else:
            name = queryName
        req = urllib2.Request(
            url='http://poj.org/userstatus?user_id=' + name,
            headers=self.headers
        )
        try:
            html = self.opener.open(req).read()
        except:
            self.wrongOJ['poj'].append(name)
            return 0
        '''
        parser all html and extract all the information
        '''
        # for submit
        submission = re.findall(r'<td align=center width=25%><a href=status\?user_id=.*?>([0-9]*?)</a>', html, re.S)
        try:
            self.submitNum+=submission[0]
        except:
            self.wrongOJ['poj']=name
            return 0
        problem = re.findall(r'p\(([0-9]*?)\)', html, re.S)
        # for AC merge all the information
        self.acArchive['poj']=self.acArchive['poj'] | set(problem)
        return submission[0],problem

    def getHDU(self,queryName=''):
        if queryName == '':
            name = self.name
        else:
            name = queryName
        req = urllib2.Request(
            url='http://acm.hdu.edu.cn/userstatus.php?user=' + name,
            headers=self.headers
        )
        try:
            html = self.opener.open(req).read()
        except:
            self.wrongOJ['hdu'].append(name)
            return 0
        '''
        parser all html and extract all the information
        '''
        submission = re.findall(r'<td>Submissions</td><td align=center>([0-9]*?)</td>', html, re.S)
        problem = re.findall('List of solved problems</font></h3>.*?<script.*?>(.*?)</script>', html, re.S)

        # for submit
        try:
            self.submitNum+=submission[0]
        except:
            self.wrongOJ['hdu']=name
            return 0
        # for AC merge all the information
        self.acArchive['hdu']=self.acArchive['hdu'] | set(problem)
        return submission[0],problem

    def getZOJ(self,queryName=''):
        if queryName == '':
            name = self.name
        else:
            name = queryName
        req = urllib2.Request(
            url='http://acm.zju.edu.cn/onlinejudge/showUserStatus.do?handle=' + name,
            headers=self.headers
        )
        try:
            html = self.opener.open(req).read()
        except:
            self.wrongOJ['hdu'].append(name)
            return 0
        '''
        parser all html and extract all the information
        '''
        submission = re.findall(r'<td>Submissions</td><td align=center>([0-9]*?)</td>', html, re.S)
        problem = re.findall('List of solved problems</font></h3>.*?<script.*?>(.*?)</script>', html, re.S)

        # for submit
        try:
            self.submitNum+=submission[0]
        except:
            self.wrongOJ['zoj']=name
            return 0
        # for AC merge all the information
        self.acArchive['zoj']=self.acArchive['zoj'] | set(problem)
        return submission[0],problem

    def getFZU(self,queryName=''):
        if queryName == '':
            name = self.name
        else:
            name = queryName
        req = urllib2.Request(
            url='http://acm.fzu.edu.cn/user.php?uname=' + name,
            headers=self.headers
        )
        try:
            html = self.opener.open(req).read()
        except:
            self.wrongOJ['fzu'].append(name)
            return 0
        '''
        parser all html and extract all the information
        '''
        submission = re.findall(r'<tr>.*?<td>Total Submitted</td>.*?<td>(.*?)</td>.*?</tr>', html, re.S)
        problem = re.findall('<b><a href="problem\.php\?pid=[0-9]*?">([0-9].*?)</a></b>', html, re.S)

        # for submit
        try:
            self.submitNum+=submission[0]
        except:
            self.wrongOJ['fzu']=name
            return 0
        # for AC merge all the information
        self.acArchive['fzu']=self.acArchive['fzu'] | set(problem)
        return submission[0],problem

if __name__ == '__main__':
    a = crawler()
    a.getInfoNoAuth()