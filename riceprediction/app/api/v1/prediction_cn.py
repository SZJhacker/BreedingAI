#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :prediction.py
@说明        :
@时间        :2021/01/13 11:05:20
'''

from flask import render_template
from app.libs.redprint import Redprint


api = Redprint('prediction_cn')

@api.route('/', endpoint='prediction_cn')
def prediction():
    return render_template('prediction_cn.html')
