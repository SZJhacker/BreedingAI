'''
Author: shenzijie
Date: 2022-10-10 09:25:33
LastEditors: shenzijie
LastEditTime: 2023-09-20 11:44:11
Email: shenzijie2013@163.com
'''
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :__init__.py
@说明        :
@时间        :2020/12/18 20:27:40
'''

from flask import Blueprint
from app.api.v1 import home, statistics, download, about, upload, features, model, predict
from app.api.v1 import home_cn, blast_cn,  about_cn, model_cn



def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__,  static_folder="static", static_url_path="/static")

    home.api.register(bp_v1, url_prefix='/')
    statistics.api.register(bp_v1)
    # stats.api.register(bp_v1)
    features.api.register(bp_v1)
    model.api.register(bp_v1)
    download.api.register(bp_v1)
    predict.api.register(bp_v1)
    upload.api.register(bp_v1)
    about.api.register(bp_v1)
    

    home_cn.api.register(bp_v1)
    blast_cn.api.register(bp_v1)
    model_cn.api.register(bp_v1)
    about_cn.api.register(bp_v1)

    return bp_v1
