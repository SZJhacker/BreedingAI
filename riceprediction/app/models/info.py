#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from sqlalchemy import Column, Integer, String
from app.models.base import Base, db

class Info(Base):
    id = Column(Integer, primary_key=True)
    article = Column(String(100))
    bioproject = Column(String(100), nullable=False)
    specie = Column(String(100), nullable=False)

    def __init__(self, article, project, specie):
        self.article = article
        self.project = project
        self.specie = specie    

    def save(self):
        db.session.add(self)
        db.session.commit()