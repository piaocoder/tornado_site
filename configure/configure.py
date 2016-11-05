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
        except ImportError:
            logging.critical('We can not find the package')
            raise ImportError

    def checkConfFile(self):
        '''
        check whether configuration file exist and can be guided properly
        configuration file is .ini which Python support initially
        :return: Boolean value check the information
        '''
        import os
        # check whether database file exist.
        configFilePath = os.path.join(os.path.dirname(__file__), "dbsetting.py")
        if os.path.isfile(configFilePath):
            self.configExist = True
            self.configFilePath = configFilePath
        else:
            infoString = 'Configuration file does not exist or set incorrect ,you will specify the options manually.'
            logging.warning(infoString)
            self.configExist=False
            self.configFilePath =None
    @staticmethod
    def checkDatabaseConnect(databaseType, databaseDriver, databaseUser,databasePassword,databaseHost,databaseName):
        try:
            from sqlalchemy import create_engine
            # according to sqlalchemy we should form that address
            # dialect[+driver]://user:password@host/dbname
            if databaseDriver == '':
                # use default driver
                sqlAddress = '%s://%s:%s@%s/%s'%(databaseType,databaseUser,databasePassword,databaseHost,databaseName)
            else:
                sqlAddress = '%s+%s://%s:%s@%s/%s'%(databaseType,databaseDriver,databaseUser,databasePassword,databaseHost,databaseName)
            print sqlAddress
            engine = create_engine(sqlAddress, echo=True)
            engine.connect()
            engine.dispose()
            return True
        except Exception as e:

            return False

    def checkDatabase(self):
        # default : MySQL
        self.checkConfFile()
        if self.configExist:
            import sqlalchemy
            try:
                import dbsetting
                databaseType = dbsetting.db_type
                databaseUser = dbsetting.db_user
                databasePassword = dbsetting.db_passwd
                databaseHost = dbsetting.db_host
                #databasePort = configParser.get('database','port')
                databaseName = dbsetting.db_name
                databaseDriver = dbsetting.db_driver
                self.databaseConnect = True
                try:
                    from sqlalchemy import create_engine
                    # according to sqlalchemy we should form that address
                    # dialect[+driver]://user:password@host/dbname
                    if databaseDriver == '':
                        # use default driver
                        sqlAddress = '%s://%s:%s@%s/%s'%(databaseType,databaseUser,databasePassword,databaseHost,databaseName)
                    else:
                        sqlAddress = '%s+%s://%s:%s@%s/%s'%(databaseType,databaseDriver,databaseUser,databasePassword,databaseHost,databaseName)
                    engine = create_engine(sqlAddress, echo=True)
                    self.databaseConnect = True
                except Exception as e:
                    logging.critical(e)
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
    def saveConfFiles(self, dbtype, driver, user,password,host,name):
        import ConfigParser
        from tornado.template import Template
        # extract string from template and form string
        configTemplatePath = os.path.join(os.path.dirname(__file__), "dbsetting.template")
        with open(configTemplatePath,'r') as templateFile:
            t = Template(templateFile.read())
            configContent = t.generate(db_host=host,db_user=user,db_passwd=password,db_type=dbtype,db_driver=driver,db_name=name)
        # write to dbsetting
        configFilePath = os.path.join(os.path.dirname(__file__), "dbsetting.py")
        with open(configFilePath,'w') as pyFile:
            pyFile.write(configContent)
        return True



if __name__ == '__main__':
    a = config()
    a.checkConfFile()