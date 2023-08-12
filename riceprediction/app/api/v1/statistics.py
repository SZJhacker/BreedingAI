#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import os
from flask import render_template
from app.libs.redprint import Redprint
from app.libs.statsplot import DataVisualization

api = Redprint('statistics')

file_path_rice = os.path.join(os.path.dirname(__file__), 'static/rice_sql_raw.csv')
file_path_soy = os.path.join(os.path.dirname(__file__), 'static/soy_sql_raw.csv')
file_path_zea = os.path.join(os.path.dirname(__file__), 'static/zea_sql_raw.csv')


@api.route('/', endpoint='statistics')
def stats():
    rice = DataVisualization(file_path_rice)
    soy = DataVisualization(file_path_soy)
    zea = DataVisualization(file_path_zea)
    ricemap = rice.draw_map('Map of rice cultivation distribution')
    soymap = soy.draw_map('Map of soybean cultivation distribution')
    zeamap = zea.draw_map('Map of zea cultivation distribution')
    map_charts = {"rice":ricemap,
                  'zea':zeamap,
                  'soy':soymap}
    sunfigs = {"rice":rice.draw_sunburst(), 'soy':soy.draw_sunburst(), 'zea':zea.draw_sunburst()}
    return render_template('statistics.html', map_charts=map_charts, sunfigs=sunfigs)
