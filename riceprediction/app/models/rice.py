#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :rice.py
@说明        :
@时间        :2020/12/23 11:08:03
'''

from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Rice(Base): 
    id = Column(Integer, primary_key=True, autoincrement=True)
    assay = Column('Genotype_assay_ID', String(50))
    accession = Column('GS_accession_name', String(50))
    country = Column('Country', String(50))
    country_cn = Column('Country_cn', String(50))
    gs_id = Column('GS_id(separated from accession)', String(50))
    sampleset = Column('SampleSet', String(50))
    subpop = Column('Subpop', String(50))
    name_cn = Column('Chinese_name', String(50))


    # 获取所有水稻的信息，不是属于某个水稻品种的信息
    # @classmethod
    # def get_accessions(cls):
    #     rice_accessions = Rice.query.with_entities(Rice.accession).all()
    #     return rice_accessions