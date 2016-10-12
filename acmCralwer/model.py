# coding:utf-8
__author__ = 'exbot'
import datetime
from sqlalchemy import Column, String, create_engine,Integer,DateTime,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class queryAccount(Base):
    # table_name :
    __tablename__ = 'user'

    # basic information
    id = Column(Integer, primary_key=True)
    mainName = Column(String(50))
    viceName = Column(String(50))
    queryTime = Column(DateTime(timezone=True),default=datetime.datetime.utcnow())

    # acm information
    pojNum = Column(Integer(5))
    hduNum = Column(Integer(5))
    zojNum = Column(Integer(5))



    def __repr__(self):
        return "<User(name='%s', fullname='%s')>" % (self.id, self.name)

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)