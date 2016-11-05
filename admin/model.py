# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    nickname = Column(String(100))
    # this is for auth

    email = Column(String(100))
    password = Column(String)

    # privilege
    manager = Boolean()