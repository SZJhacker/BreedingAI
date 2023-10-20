#!/usr/bin/env python3
# -*- coding=utf-8 -*-


from sqlalchemy import Column, Integer, String
from app.models.base import Base, db

class NewData(Base):
    id = Column(Integer, primary_key=True)
    phenotype = Column(String(50), nullable=False)
    specie = Column(String(50), nullable=False)
    reference_genome = Column(String(50), nullable=False)
    planting_region = Column(String(50))
    planting_year = Column(String(50))
    filename = Column(String(100), nullable=False)

    def __init__(self, phenotype, specie, reference_genome, planting_region, planting_year, filename):
        self.phenotype = phenotype
        self.specie = specie
        self.reference_genome = reference_genome
        self.planting_region = planting_region
        self.planting_year = planting_year
        self.filename = filename
    def save(self):
        db.session.add(self)
        db.session.commit()
