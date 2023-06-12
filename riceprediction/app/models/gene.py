#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from app.models.base import Base

class RiceGenes(Base):
    __tablename__ = 'ricegene'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rap = Column('RAP', String(50), default='None')
    mus = Column('MSU', String(300), default='None')
    # description = Column('Description', String(600))

class ZeaGenes(Base):
    __tablename__ = 'zeagenes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    v5 = Column('B73_V5', String(30), default='None')
    v4 = Column('B73_V4', String(30), default='None')
    v3 = Column('B73_V3', String(30), default='None')
    symbol = Column('Gene_Symbol', String(30), default='None')
    fullname = Column('Full_Name', String(50), default='None')

class SoyGenes(Base):
    __tablename__ = 'soygenes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    v1 = Column('Glyma1.1', String(30), default='None')
    v2 = Column('Glyma2.0', String(30), default='None')