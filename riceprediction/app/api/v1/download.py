#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os, json
from flask import render_template, request, jsonify
from app.libs.redprint import Redprint
from app.libs.Info import Info

api = Redprint('download')

def rice():
    file_path = os.path.join(os.path.dirname(__file__), 'static/summary_clean.csv')
    rice_pheno = Info(file_path)
    return rice_pheno

def zea():
    pass

def soy():
    pass

swither = {
    'rice': rice,
    'zea' : zea,
    'soy' : soy,
}


@api.route('/<spiece>/', endpoint='download', methods=['POST','GET'])
def download(spiece):
    pheno = request.form.get('data', 'Whiteness_Degree_of_Complete_Grain(%)')
    crop = swither[spiece]()
    phenotable = crop.construct_table(pheno).fillna('-')
    graphJSON = crop.plot_histogram(pheno=pheno) # 返回分布图的json
    if request.method == 'POST':
        json_table = json.dumps(phenotable.to_dict('split'))
        return jsonify(fig=graphJSON, table=json_table)
    return render_template('download.html', phenos=crop.labels, phenotable=phenotable, graphJSON=graphJSON, spiece=spiece)