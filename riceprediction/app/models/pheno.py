'''
Author: shenzijie
Date: 2022-10-10 10:22:43
LastEditors: shenzijie
LastEditTime: 2022-11-08 12:19:14
Email: shenzijie2013@163.com
'''
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :.py
@说明        :
@时间        :2021/01/20 16:04:23
'''

from sqlalchemy import Column, Integer, Float,ForeignKey, String
from sqlalchemy.orm import relationship
from app.models.base import Base


class Pheno(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column('Sample_ID', String(20))
    bioproj = Column('Bioproject', String(20))
    name_cn = Column('Name_cn', String(20))
    name = Column('Name', String(20))
    white_complete_grain = Column('Whiteness_Degree_of_Complete_Grain', Float(8))
    white_dead_grain = Column('Whiteness_Degree_of_Dead_Grain', Float(8))
    amylose_content = Column('Amylose_Content_of_Grain', Float(8))
    protein_content = Column('Protein_Content_of_Grain', Float(8))
    taste_score = Column('Taste_Score_of_Cooked_Grain', Float(8))
    water_content = Column('Water_Content_of_Grain', Float(8))
    awn_len = Column('Awn_Length', Float(8))
    grain_len = Column('Grain_Length', Float(8))
    grain_wid = Column('Grain_Width', Float(8))
    grain_thick = Column('Grain_Thickness', Float(8))
    k_grain_weight = Column('1000_Grain_Weight', Float(8))
    heading_date = Column('Heading_Date', String(16))
    flag_leaf_len = Column('Flag_Leaf_Length', Float(8))
    flag_leaf_wid = Column('Flag_Leaf_Width', Float(8))
    leaf_blade_wid = Column('Leaf_Blade_Width', Float(8))
    leaf_sheath_color = Column('Leaf_sheath_color', String(20))
    plant_height = Column('Plant_Height', Float(8))
    panicle_len = Column('Panicle_Length', Float(8))
    culm_len = Column('Culm_Length', Float(8))
    SPAD_flag = Column('SPAD_Value_of_Flag_Leaf', Float(8))
    tiller_num = Column('Tiller_Number_per_Plant', Float(8))
    blighted_grain_per_plant = Column('Blighted_Grains_per_Plant', Float(8))
    blighted_grain_per_panicle = Column('Blighted_Grains_per_Panicle', Float(8))
    blighted_grain_weight_per_plant = Column('Blighted_Grains_Weight_per_Plant', Float(8))
    filled_grain_per_plant = Column('Filled_Grains_per_Plant', Float(8))
    filled_grain_per_panicle = Column('Filled_Grains_Per_Panicle', Float(8))
    filled_grain_weight_per_plant = Column('Filled_Grains_Weight_per_Plant', Float(8))
    grain_per_panicle = Column('Grain_Number_per_Panicle', Float(8))
    seed_setting = Column('Seed_Setting_Rate',Float(8))
    grain_yield = Column('Grain_Yield_per_Plant', Float(8))
    panicles = Column('Panicle_Number_per_Plant', Float(8)) 
    panicles_effective = Column('Number_of_Productive_Panicle_per_Plant', Float(8))
    panicles_weight = Column('Panicle_Weight', Float(8))
    spikelet_per_panicle = Column('Spikelet_Number_per_Panicle', Float(8))
    panicle_weight_per_plant = Column('Panicle_Weight per Plant', Float(8))
    yield_plant = Column('Yield_per_Plant',Float(8))
    Cd_concentration = Column('Cd_concentration', Float(8))
    treatment = Column('Treatment', String(20))
    year = Column('Years', String(20))
    region = Column('Region', String(20))
    
    @classmethod
    def search_by_pheno(cls, pheno_name):
        pass


