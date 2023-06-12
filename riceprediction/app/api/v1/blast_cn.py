#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :blast.py
@说明        :
@时间        :2021/01/13 10:31:13
'''
from flask import render_template
from app.libs.redprint import Redprint


api = Redprint('blast_cn')

@api.route('/', endpoint='blast_cn')
def blast_cn():
    return render_template('blast_cn.html')