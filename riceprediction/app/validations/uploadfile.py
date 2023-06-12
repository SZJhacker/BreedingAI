#!/usr/bin/env python3
# -*- coding=utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

# 定义表单类
class UploadForm(FlaskForm):
    phenotype = StringField('Phenotype', validators=[DataRequired()])
    specie = StringField('Specie', validators=[DataRequired()])
    reference_genome = StringField('Reference Genome', validators=[DataRequired()])
    planting_region = StringField('Planting Region')
    planting_year = StringField('Planting Year')
    file = FileField('File', validators=[DataRequired()])