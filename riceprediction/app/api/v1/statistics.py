#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import os
# import json, plotly
# import pandas as pd
# import plotly.express as px
from flask import render_template
from app.libs.redprint import Redprint
from app.libs.statsplot import DataVisualization
# from pyecharts import options as opts
# from pyecharts.charts import Map
# import plotly.graph_objs as go

api = Redprint('statistics')

file_path_rice = os.path.join(os.path.dirname(__file__), 'static/rice_sql_raw.csv')
file_path_zea = os.path.join(os.path.dirname(__file__), 'static/zea_sql_raw.csv')


@api.route('/', endpoint='statistics')
def stats():
    rice = DataVisualization(file_path_rice)
    zea = DataVisualization(file_path_zea)
    map_charts = {"rice":rice.draw_map('Map of rice cultivation distribution')}
    sunfigs = {"rice":rice.draw_sunburst(),'zea':zea.draw_sunburst()}
    return render_template('statistics.html', map_charts=map_charts, sunfigs=sunfigs)
