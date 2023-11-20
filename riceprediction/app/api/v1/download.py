#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os, json
from flask import render_template, request, jsonify
from app.libs.redprint import Redprint
# from app.libs.Info import Info
from app.libs.statsplot import DataVisualization

api = Redprint('download')

def process(file_path, phenoname, species):
    pheno = DataVisualization(file_path)
    # pheno = Info(file_path)
    gvcftable = pheno.construct_table(phenoname, species=species, datatype='gvcf', suffix='raw.g.vcf.gz').fillna('-')
    vcftable = pheno.construct_table(phenoname, species=species, datatype='vcf', suffix='filtered.snp.vcf.gz').fillna('-')
    gsctable = pheno.construct_table(phenoname, species=species, datatype='gsctool', suffix='gsctool.csv').fillna('-')
    graphJSON = pheno.plot_histogram(pheno=phenoname) # 返回分布图的json
    return (pheno, [gvcftable, vcftable, gsctable], graphJSON)

def rice():
    file_path = os.path.join(os.path.dirname(__file__), 'static/rice_sql_raw.csv')
    phenoname = request.form.get('data', 'Whiteness Degree of Complete Grain (%)')
    return process(file_path, phenoname, 'rice')

def soy():
    file_path = os.path.join(os.path.dirname(__file__), 'static/soy_sql_raw.csv')
    phenoname = request.form.get('data', 'Number of one seed per pod')
    return process(file_path, phenoname, 'soy')

def zea():
    file_path = os.path.join(os.path.dirname(__file__), 'static/zea_sql_raw.csv')
    phenoname = request.form.get('data', 'Upper leaf number')
    return process(file_path, phenoname, 'zea')

swither = {
    'rice': rice,
    'zea' : zea,
    'soy' : soy,
}


@api.route('/<species>/', endpoint='download', methods=['POST','GET'])
def download(species):
    crop, phenotable, graphJSON = swither[species]()
    if request.method == 'POST':
        json_table = json.dumps([i.to_dict('split') for i in phenotable])
        return jsonify(fig=graphJSON, table=json_table)
    return render_template('download.html', phenos=crop.labels, phenotable=phenotable, graphJSON=graphJSON, species=species)