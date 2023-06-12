#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Length
from wtforms.widgets.html5 import SearchInput
from wtforms.widgets import SubmitInput

# 中文版
class SearchCN(FlaskForm):
    accession = StringField('', validators=[Length(min=1, max=30)], widget=SearchInput(), render_kw={"class":"orm-control me-sm-2", "placeholder":"品种名称"})
    # submit = SubmitField('搜索', widget=SubmitInput(), render_kw={"class":"btn btn-secondary my-2 my-sm-0 form-group"})

# 英文版
class Search(FlaskForm):
    accession = StringField(validators=[Length(min=1, max=30)])
