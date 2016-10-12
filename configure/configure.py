# coding=utf-8
__author__ = 'exbot'

'''
This is the configuration file that show some vital information such as
* database's account , password , host , port and name
* the discription of the whole site
'''
import logging


class config:
    def __init__(self):
        pass

    def checkConfFile(self):
        '''
        check whether configuration file exist and can be guided properly
        configuration file is .ini which Python support initially
        :return: Boolean value check the information
        '''
        try:
            import ConfigParser
            import os
        except ImportError:
            logging.error('We can not find the package')
            raise ImportError
        except Exception as e:
            errorInfo='''Woo we do not know what happened exactly.
            please tell me at github , thanks.
            '''
            logging.error(errorInfo)
            raise e
        # check whether config file exist.
        configFilePath = os.path.join(os.path.dirname(__file__), "config.ini")





    def checkDatabase(self):
        # default : MySQL
        pass