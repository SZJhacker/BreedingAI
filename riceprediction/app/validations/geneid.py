#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class Geneid(FlaskForm):
    genes = TextAreaField('Gene names', validators=[DataRequired(message='Please input your Gene names')])
    submit = SubmitField('Submit')
