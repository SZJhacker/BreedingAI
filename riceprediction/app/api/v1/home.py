#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :home.py
@说明        :
@时间        :2020/12/25 20:24:20
'''

from flask import render_template
from app.libs.redprint import Redprint


api = Redprint('home')

@api.route('/')
def index():

    return render_template('home.html')
