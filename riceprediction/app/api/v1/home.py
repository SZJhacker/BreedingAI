#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :home.py
@说明        :
@时间        :2020/12/25 20:24:20
'''
import os
import pandas as pd
from flask import render_template
from app.libs.redprint import Redprint
from pyecharts import options as opts
from pyecharts.charts import Map

api = Redprint('home')

file_path = os.path.join(os.path.dirname(__file__), 'static/rice_summary.csv')


@api.route('/')
def index():
    province_dic = {
        'Beijing': '北京市',
        'Beishan': '湖南省',
        'Haerbin': '黑龙江省',
        'Hainan': '海南省',
        'Hangzhou': '浙江省',
        'Heihe': '黑龙江省',
        'Japan': '日本',
        'Jiamusi': '黑龙江',
        'Jilin': '吉林省',
        'Lingshui': '海南省',
        'Minzhu': '黑龙江省',
        'Sanya': '海南省',
        'Shanghai': '上海市',
        'Shenzhen': '广东省',
        'Wenjiang': '四川省',
        'Wuchang': '湖北省',
        'Wuhan': '湖南省',
        'Yangzhou': '江苏省'
    }
    pheno = pd.read_csv(file_path, usecols=['Region', 'Counts'])
    pheno['Region_cn'] = pheno['Region'].replace(province_dic)
    df = pheno[['Region_cn','Counts']].groupby(['Region_cn'])['Counts'].sum().reset_index(name='Counts')
    map_data = [(p, c) for p, c in zip(df['Region_cn'], df['Counts'])]
    map_chart = Map(init_opts=opts.InitOpts(theme='light'))

    # 添加数据
    map_chart.add("水稻种植数目", data_pair=map_data, maptype="china", is_map_symbol_show=False, aspect_scale=0.85, zoom=1.4,
                    pos_left='15%', pos_right='15%', pos_top='20%', map_value_calculation = "sum")

    # 设置地图样式和配置项
    map_chart.set_series_opts(
        label_opts=opts.LabelOpts(is_show=True, formatter="{b}"))
    # map_chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    map_chart.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(min_=0, max_=df['Counts'].max().item(), pos_left='right', range_color=['lightskyblue', 'yellow', 'orangered'])
    )

    return render_template('home.html', map_charts=map_chart.dump_options())
