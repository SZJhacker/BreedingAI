#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :search.py
@说明        :
@时间        :2021/01/13 11:04:41
'''

from flask import render_template, request
from app.libs.redprint import Redprint
from app.models.rice import Rice
from app.validations.search import SearchCN

api = Redprint('search_cn')

@api.route('/', endpoint='search_cn')
def search_cn():
    search = SearchCN()
    page = int(request.args.get('page',1))
    per_page = 20
    pagination = Rice.query.paginate(page, per_page, error_out=False)
    accession = request.args.get('accession')
    if accession:
        pagination = Rice.query.filter(Rice.accession.contains(accession.strip())).paginate(page, per_page, error_out=False)
    return render_template('search_cn.html', form=search, pagination=pagination)