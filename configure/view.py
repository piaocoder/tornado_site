#coding=utf-8
__author__ = 'exbot'

import tornado.web
import configure
class configureHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        conf = configure.config()
        conf.runTest()
        if conf.configExist and conf.databaseConnect :
            raise tornado.web.HTTPError(403)
        else:
            self.render('configure/changeConf.html',error=False)

    def post(self, *args, **kwargs):
        conf = configure.config()
        conf.runTest()
        if conf.configExist and conf.databaseConnect :
            # if configure successfully just return false
            raise tornado.web.HTTPError(403)
        else:
            pass
        databaseType = self.get_argument('databaseType')
        databaseUser = self.get_argument('databaseUser')
        databasePassword = self.get_argument('databasePassword')
        databaseHost = self.get_argument('databaseHost')
        databaseName = self.get_argument('databaseName')
        databaseDriver = self.get_argument('databaseDriver')

        flag = configure.config.checkDatabaseConnect(databaseType,databaseDriver,databaseUser,databasePassword,databaseHost,databaseName)
        if flag:
            # it can used!
            conf.saveConfFiles(databaseType,databaseDriver,databaseUser,databasePassword,databaseHost,databaseName)
            # finished...
            self.render('configure/result.html',)
        else:
            self.render('configure/changeConf.html',error=True)

    def write_error(self, status_code, **kwargs):
        self.render('configure/error.html',status_code=status_code)