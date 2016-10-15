#coding=utf-8
__author__ = 'exbot'
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

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



if __name__ == "__main__":
    tornado.options.parse_command_line()

    # check initial information
    from configure import configure,setting,uimodule
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
            (r"^/configure/",'configure.view.configureHandler'),
            (r"^/query/",'acmCralwer.view.queryIndexHandler')

        ],
        ui_modules={
            'getSetting':uimodule.settingOptionModule,
        },
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
    )
    if hasattr(setting, "LOGFILE") and setting.LOGFILE:
        import logging
        from logging import StreamHandler
        from logging.handlers import RotatingFileHandler,SMTPHandler

        logFilePath = 'log/site.log'

        file_handler = RotatingFileHandler(logFilePath, 'a',1 * 1024 * 1024, 10)

        RootLogger = logging.getLogger()

        # We have a File_handler so we don't need streamhandler
        for handler in RootLogger.handlers:
            # There are some Handler is a subclass of streamhandler
            # SO, using the type instead isinstance
            if type(handler) is StreamHandler:
                RootLogger.removeHandler(handler)

        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))

        RootLogger.addHandler(file_handler)
        if hasattr(setting, "MAIL_SERVER"):
            credentials = None
            if setting.MAIL_USERNAME and setting.MAIL_PASSWORD:
                credentials = (setting.MAIL_USERNAME, setting.MAIL_PASSWORD)
                mail_handler = SMTPHandler((setting.MAIL_SERVER,setting.MAIL_PORT),
                                            setting.MAIL_USERNAME,
                                            setting.ADMINS, "站点出错了！",
                                            credentials,secure=True)
            mail_handler.setLevel(logging.ERROR)
            RootLogger.addHandler(mail_handler)


    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()