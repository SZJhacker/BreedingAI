#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :jbrowser.py
@说明        :
@时间        :2021/01/13 11:04:19
'''

from flask import render_template, url_for
from app.libs.redprint import Redprint



api = Redprint('jbrowse')

@api.route('/')
def jbrowse():
    return render_template('jbrowse.html')