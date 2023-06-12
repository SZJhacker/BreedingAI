#!/usr/bin/env python3
# -*- coding=utf-8 -*-

'''
Author: shenzijie
Date: 2022-10-09 21:56:51
LastEditors: shenzijie
LastEditTime: 2022-11-21 23:53:06
'''
import os, json
from flask import render_template, request
from app.libs.redprint import Redprint
from app.libs.Info import Info


api = Redprint('stats')

file_path = os.path.join(os.path.dirname(__file__), 'static/summary_clean.csv')
rice_pheno = Info(file_path)

@api.route('/histogram/', methods=['GET', 'POST'], endpoint='histogram')
def histogram():
    return rice_pheno.plot_histogram(request.args['data'])
    

@api.route('/', endpoint='stats')
def stats():
    # if request.method == 'POST':
    phenos = rice_pheno.labels
    graphJSON_distri = rice_pheno.plot_distr()
    graphJSON_ratio = rice_pheno.plot_pie()
    graphJSON_hist = rice_pheno.plot_histogram()
    return render_template('stats.html', phenos=phenos, graphJSON_distri=graphJSON_distri, graphJSON_ratio=graphJSON_ratio, graphJSON_hist=graphJSON_hist)
