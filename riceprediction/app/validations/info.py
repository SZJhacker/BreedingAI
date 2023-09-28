#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InfoForm(FlaskForm):
    article = StringField('Article')
    bioproject = StringField('BioProject', validators=[DataRequired()])
    specie = StringField('Specie', validators=[DataRequired()])
    submit = SubmitField('Submit')
