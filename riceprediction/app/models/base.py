#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :base.py
@说明        :
@时间        :2021/01/20 16:22:14
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, SmallInteger


db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True # 阻止创建Base表
    status = Column(SmallInteger, default=1)
