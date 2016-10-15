# coding=utf-8
__author__ = 'exbot'

'''
This is the configuration file that show some vital information such as
* database's account , password , host , port and name
* the discription of the whole site
'''
import logging
import os

class config:
    '''
    this is configuration file,it will check all the information site needs and export a dictionary which will use in website.
    '''
    configExist = False
    databaseConnect = False
    configFilePath = None
    def __init__(self):
        pass

    def checkRequirement(self):
        '''
        check all the requirement in setting
        :return:
        '''
        try:
            import ConfigParser
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
            self.configFilePath = configFilePath
        else:
            infoString = 'Configuration file does not exist or set incorrect ,you will specify the options manually.'
            logging.warning(infoString)
            self.configExist=False
            self.configFilePath  =None

    def checkDatabase(self):
        # default : MySQL
        if self.configExist:
            import ConfigParser
            import sqlalchemy
            configParser = ConfigParser.ConfigParser()
            configParser.read(self.configFilePath)
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
                    logging.info("Database version : %s " % data[0])
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

    #set up a new ini file
    def saveConfFiles(self,type,user,password,host,name):
        import ConfigParser
        configFilePath = os.path.join(os.path.dirname(__file__), "config.ini")
        cf = ConfigParser.ConfigParser()
        # add database section
        cf.add_section('database')
        cf.set('database','type',type)
        cf.set('database','user',user)
        cf.set('database','password',password)
        cf.set('database','host',host)
        cf.set('database','name',name)
        cf.write(open(configFilePath, "w"))
        return True

    def testDatabaseConnect(self,type,user,password,host,name):
        # default : MySQL
        if 1:
            import ConfigParser
            import sqlalchemy
            configParser = ConfigParser.ConfigParser()
            try:
                databaseType = type
                databaseUser = user
                databasePassword = password
                databaseHost = host
                databaseName = name
                if databaseType == 'MySQL':
                    import MySQLdb
                    con = MySQLdb.connect(databaseHost,databaseUser,databasePassword,databaseName)
                    cur = con.cursor()
                    cur.execute("SELECT VERSION()")
                    verData = cur.fetchone()
                    print verData
                    #logging.info("Database version : %s ") % verData[0]
                    con.close()
                    return verData[0]
                elif databaseType == 'SQLite':
                    import sqlite3
                    import os
                    sqliteParentDir =os.path.abspath(os.path.join(os.path.dirname('main.py'),os.path.pardir))
                    sqliteFilePath = os.path.join(sqliteParentDir,'%s.db') %(databaseName)
                    conn = sqlite3.connect(sqliteFilePath)
                    conn.close()
                    verData = 'sqlite'
                    return verData
                else:
                    logging.critical('we do not support your database,our supported database type is:MySQL,SQLite(match case)')
                    return False


            except Exception as e:
                logging.critical(e)
                return False
        else:
            pass



if __name__ == '__main__':
    a = config()
    a.checkConfFile()