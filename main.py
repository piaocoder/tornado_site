__author__ = 'exbot'
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
from configure import configure
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
import logging
# enable jinja2

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')
    def write_error(self, status_code, **kwargs):
        self.write("Gosh darnit, user! You caused a %d error." % status_code)

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
            raise tornado.web.HTTPError(403)
        else:
            pass
        databaseType = self.get_argument('databaseType')
        databaseUser = self.get_argument('databaseUser')
        databasePassword = self.get_argument('databasePassword')
        databaseHost = self.get_argument('databaseHost')
        databaseName = self.get_argument('databaseName')
        conf = configure.config()
        ver = conf.testDatabaseConnect(databaseType,databaseUser,databasePassword,databaseHost,databaseName)
        print ver
        if ver:
            conf.saveConfFiles(databaseType,databaseUser,databasePassword,databaseHost,databaseName)
            # finished...
            self.render('configure/result.html',ver=ver)
        else:
            self.render('configure/changeConf.html',error=True)

    def write_error(self, status_code, **kwargs):
        self.render('configure/error.html',status_code=status_code)

if __name__ == "__main__":
    tornado.options.parse_command_line()

    # check initial information
    conf = configure.config()
    conf.runTest()

    # setting
    settings = {
        "xsrf_cookies": True,
        "login_url": "/login",
    }
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"^/configure/",configureHandler),
            (r"^/query/",'acmCralwer.view.queryHandler')

        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()