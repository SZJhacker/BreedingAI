#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px


class DataVisualization:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file, dtype={'Years': str})
        self.com_cols = ['Sample_ID', 'Bioproject', 'Name_cn', 'Name', 'Years', 'Region', 'Region_cn']
        self.data['Counts'] = self.data.drop(columns=self.com_cols).count(axis=1)

    @staticmethod
    def _figjson(fig):
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def build_hierarchical_dataframe(totol_name, phenos):
        sun_tree = pd.DataFrame(columns=['id', 'parent', 'counts'])
        sun_tree['id'] = phenos.index
        sun_tree['counts'] = phenos.values
        sun_tree['parent'] = totol_name
        sun_tree.loc[len(sun_tree)] = [totol_name, '', sun_tree['counts'].sum()]
        return sun_tree

    def draw_map(self, title):
        map_data_pre = self.data[['Region_cn', 'Counts']].groupby(['Region_cn'])['Counts'].sum().reset_index(name='Counts')
        map_data = [(p, c) for p, c in zip(map_data_pre['Region_cn'], map_data_pre['Counts'])]
        map_chart = Map(init_opts=opts.InitOpts(theme='light'))
        map_chart.add(title, data_pair=map_data, maptype="china", is_map_symbol_show=False, aspect_scale=0.85,
                      zoom=1.4, pos_left='15%', pos_right='15%', pos_top='20%', map_value_calculation="sum")
        map_chart.set_series_opts(label_opts=opts.LabelOpts(is_show=True, formatter="{b}"))
        map_chart.set_global_opts(
            visualmap_opts=opts.VisualMapOpts(min_=0, max_=map_data_pre['Counts'].max().item(), pos_left='right',
                                              range_color=['lightskyblue', 'yellow', 'orangered'])
        )
        json_result = map_chart.dump_options_with_quotes()
        return json_result

    def draw_sunburst(self):
        total_name = 'Total genome-pheno pairs'
        df_years = self.data[['Years', 'Counts']]
        df_years = df_years.groupby('Years')['Counts'].sum()
        sun_trees = self.build_hierarchical_dataframe(total_name, df_years)

        sunfig = go.Figure()
        sunfig.add_trace(go.Sunburst(
            labels=sun_trees['id'],
            parents=sun_trees['parent'],
            values=sun_trees['counts'],
            branchvalues='total',
            hovertemplate='<b>%{label} </b> <br> Sales: %{value}<br>',
            textinfo='label+value',
            marker=dict(colors=px.colors.qualitative.Pastel)
        ))

        sunfig.update_layout(margin=dict(t=10, l=10, r=10, b=10))
        return self._figjson(sunfig)
