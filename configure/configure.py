# coding=utf-8
__author__ = 'exbot'

'''
This is the configuration file that show some vital information such as
* database's account , password , host , port and name
* the discription of the whole site
'''
import logging


class config:
    '''
    this is configuration file,it will check all the information site needs and export a dictionary which will use in website.
    '''
    configExist = False
    databaseConnect = False

    def __init__(self):
        pass

    def checkRequirement(self):
        '''
        check all the requirement in setting
        :return:
        '''
        try:
            import ConfigParser
            import os
            import sqlalchemy
            import MySQLdb
            import sqlite3
        except ImportError:
            logging.critical('We can not find the package')
            raise ImportError

    def checkConfFile(self):
        '''
        check whether configuration file exist and can be guided properly
        configuration file is .ini which Python support initially
        :return: Boolean value check the information
        '''
        try:
            import os
        except ImportError:
            logging.critical('We can not find the package')
            raise ImportError
        except Exception as e:
            errorInfo='''Woo we do not know what happened exactly.
            please tell me at github , thanks.
            '''
            logging.critical(errorInfo)
            raise e
        # check whether config file exist.
        configFilePath = os.path.join(os.path.dirname(__file__), "config.ini")
        if os.path.isfile(configFilePath):
            self.configExist = True
        else:
            infoString = 'Configuration file does not exist or set incorrect ,you will specify the options manually.'
            logging.warning(infoString)




    def checkDatabase(self):
        # default : MySQL
        if self.configExist:
            import ConfigParser
            import sqlalchemy
            configParser = ConfigParser.ConfigParser()
            try:
                databaseType = configParser.get('database','type')
                databaseUser = configParser.get('database','user')
                databasePassword = configParser.get('database','password')
                databaseHost = configParser.get('database','host')
                #databasePort = configParser.get('database','port')
                databaseName = configParser.get('database','name')
                self.databaseConnect = True
                if databaseType == 'MySQL':
                    import MySQLdb
                    con = MySQLdb.connect(databaseHost,databaseUser,databasePassword,databaseName)
                    cur = con.cursor()
                    cur.execute("SELECT VERSION()")
                    data = cur.fetchone()
                    logging.info("Database version : %s ") % data
                    con.close()
                elif databaseType == 'SQLite':
                    import sqlite3
                    import os
                    sqliteParentDir =os.path.abspath(os.path.join(os.path.dirname('main.py'),os.path.pardir))
                    sqliteFilePath = os.path.join(sqliteParentDir,'%s.db') %(databaseName)
                    conn = sqlite3.connect(sqliteFilePath)
                    conn.close()
                else:
                    logging.critical('we do not support your database,our supported database type is:MySQL,SQLite(match case)')
                    self.databaseConnect = False


            except Exception as e:
                logging.warning('Your configuration file is not valid , please set by yourself.')
                logging.warning(e)
                self.databaseConnect = False
        else:
            pass

    def runTest(self):
        self.checkRequirement()
        self.checkConfFile()
        self.checkDatabase()

if __name__ == '__main__':
    a = config()
    a.checkConfFile()