#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :prediction.py
@说明        :
@时间        :2021/01/13 11:05:20
'''

from flask import render_template
from app.libs.redprint import Redprint


api = Redprint('model_cn')

@api.route('/', endpoint='model_cn')
def model_cn():
    return render_template('model_cn.html')
