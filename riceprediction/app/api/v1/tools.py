#!/usr/bin/env python3
# -*- coding=utf-8 -*-

'''
Author: shenzijie
Date: 2022-10-20 11:18:56
LastEditors: shenzijie
LastEditTime: 2022-11-05 20:46:30
Email: shenzijie2013@163.com
'''
import  re
from flask import render_template, request
from app.libs.redprint import Redprint
from app.validations.geneid import Geneid
from app.models.gene import RiceGenes, ZeaGenes, SoyGenes
from sqlalchemy import or_

api = Redprint('tools')

def split(genes):
    return re.split('[,\s]+', genes)

def rice(genes):
    values = split(genes)
    results = RiceGenes.query.filter(or_(RiceGenes.rap.in_(values), RiceGenes.mus.in_(values))).all()
    return results

def zea(genes):
    values = split(genes)
    results = ZeaGenes.query.filter(or_(ZeaGenes.v5.in_(values), 
                                        ZeaGenes.v4.in_(values), 
                                        ZeaGenes.v3.in_(values), 
                                        ZeaGenes.symbol.in_(values), 
                                        ZeaGenes.fullname.in_(values))).all()
    return results

def soy(genes):
    values = split(genes)
    results = SoyGenes.query.filter(or_(SoyGenes.v2.in_(values), SoyGenes.v1.in_(values))).all()
    return results

@api.route('/', endpoint='tools', methods=['GET', 'POST'])
def tools():
    form = Geneid(request.form)
    if form.validate_on_submit():
        page = int(request.args.get('page', 1))
        per_page = 20
        spieceid = request.args.get('formid', 1, type=int)
        switcher = {
            1 : rice,
            2 : zea,
            3 : soy
        }
        genes = form.genes.data.strip()
        results = switcher[spieceid](genes)
        return render_template('geneid.html', formid=spieceid, genes=results)
    return render_template('tools.html', form=form)

