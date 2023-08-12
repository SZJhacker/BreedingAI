#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os, json
from flask import render_template, request, jsonify
from app.libs.redprint import Redprint
from app.libs.Info import Info
from app.libs.statsplot import DataVisualization

api = Redprint('download')

def process(file_path, phenoname):
    pheno = DataVisualization(file_path)
    # pheno = Info(file_path)
    phenotable = pheno.construct_table(phenoname).fillna('-')
    graphJSON = pheno.plot_histogram(pheno=phenoname) # 返回分布图的json
    return (pheno, phenotable, graphJSON)

def rice():
    file_path = os.path.join(os.path.dirname(__file__), 'static/rice_sql_raw.csv')
    phenoname = request.form.get('data', 'Whiteness Degree of Complete Grain (%)')
    return process(file_path, phenoname)

def soy():
    file_path = os.path.join(os.path.dirname(__file__), 'static/soy_sql_raw.csv')
    phenoname = request.form.get('data', 'Number of one seed per pod')
    return process(file_path, phenoname)

def zea():
    file_path = os.path.join(os.path.dirname(__file__), 'static/zea_sql_raw.csv')
    phenoname = request.form.get('data', 'Upper leaf number')
    return process(file_path, phenoname)

swither = {
    'rice': rice,
    'zea' : zea,
    'soy' : soy,
}


@api.route('/<spiece>/', endpoint='download', methods=['POST','GET'])
def download(spiece):
    crop, phenotable, graphJSON = swither[spiece]()
    if request.method == 'POST':
        json_table = json.dumps(phenotable.to_dict('split'))
        return jsonify(fig=graphJSON, table=json_table)
    return render_template('download.html', phenos=crop.labels, phenotable=phenotable, graphJSON=graphJSON, spiece=spiece)