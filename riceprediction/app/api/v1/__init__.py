'''
Author: shenzijie
Date: 2022-10-10 09:25:33
LastEditors: shenzijie
LastEditTime: 2023-07-14 00:54:42
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
from app.api.v1 import home, statistics, prediction, download, about, g2p, upload
from app.api.v1 import home_cn, blast_cn,  prediction_cn, about_cn


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__,  static_folder="static", static_url_path="/static")

    home.api.register(bp_v1, url_prefix='/')
    statistics.api.register(bp_v1)
    # stats.api.register(bp_v1)
    g2p.api.register(bp_v1)
    prediction.api.register(bp_v1)
    download.api.register(bp_v1)
    upload.api.register(bp_v1)
    about.api.register(bp_v1)
    

    home_cn.api.register(bp_v1)
    blast_cn.api.register(bp_v1)
    prediction_cn.api.register(bp_v1)
    about_cn.api.register(bp_v1)

    return bp_v1
