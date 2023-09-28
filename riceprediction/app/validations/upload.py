#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileSize
from wtforms import  SubmitField, FileField, SelectField, StringField
from wtforms.validators import DataRequired


class UploadFile(FlaskForm):
    file = FileField(
        'Please upload a gzip-compressed VCF file with a maximum file size of 100MB.',
        validators=[FileRequired(),
                    FileAllowed(['gz'], 'Gzip-compressed Files Only!'),
                    FileSize(max_size=100 * 1024 * 1024, message='File size should be less than 100 MB')])
    species = SelectField(
        'Species',  # 显示的标签
        choices=[('rice', 'Rice'), ('soybean', 'Soybean'), ('zea', 'Zea')],  # 选项列表
        default='rice'  # 默认选项
    )
    submit = SubmitField('Submit')


class UploadForm(UploadFile):
    file = FileField('File', validators=[DataRequired()])
    phenotype = StringField('Phenotype', validators=[DataRequired()])
    # specie = StringField('Specie', validators=[DataRequired()])
    reference_genome = StringField('Reference Genome', validators=[DataRequired()])
    planting_region = StringField('Planting Region')
    planting_year = StringField('Planting Year')