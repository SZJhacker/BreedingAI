#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map, Tab
import json, plotly
import plotly.graph_objects as go
import plotly.express as px


class DataVisualization:
    tab = Tab()
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file, dtype={'Years': str})
        self.com_cols = ['Sample_ID', 'Bioproject', 'Name_cn', 'Name', 'Treatment', 'Years', 'location', 'Region', 'Region_cn']
        self.pheno = self.data.drop(columns=self.com_cols)
        self.pheno_stats = self.data.drop(columns=self.com_cols).count()
        self.data['Counts'] = self.data.drop(columns=self.com_cols).count(axis=1)
        self.labels = self.pheno_stats.index
        self.counts = self.pheno_stats.values

        self.ftp_temp = 'https://ibi.zju.edu.cn/BreedingAI/{species}/{datatype}/{sampleid}_{suffix}'

        self.sunfig = go.Figure()
        self.map_chart = Map(init_opts=opts.InitOpts(theme='light'))

    @staticmethod
    def __figjson(fig):
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
        map_data_pre = self.data[['Region', 'Counts']].groupby(['Region'])['Counts'].sum().reset_index(name='Counts')
        map_data = [(p, c) for p, c in zip(map_data_pre['Region'], map_data_pre['Counts'])]
        # map_chart = Map(init_opts=opts.InitOpts(theme='light'))
        self.map_chart.add(title, data_pair=map_data, maptype="china", is_map_symbol_show=False, aspect_scale=0.9,
                      zoom=1.2, pos_left='10%', pos_right='10%', pos_top='10%', map_value_calculation="sum")
        self.map_chart.set_series_opts(label_opts=opts.LabelOpts(is_show=True, formatter="{b}"))
        self.map_chart.set_global_opts(
            visualmap_opts=opts.VisualMapOpts(min_=0, max_=map_data_pre['Counts'].max().item(), pos_left='right',
                                              range_color=['lightskyblue', 'yellow', 'orangered'])
        )
        json_result = self.map_chart.dump_options_with_quotes()
        return json_result
    
    def draw_sunburst(self):
        total_name = 'Total genome-pheno pairs'
        df_years = self.data[['Years', 'Counts']]
        df_years = df_years.groupby('Years')['Counts'].sum()
        sun_trees = self.build_hierarchical_dataframe(total_name, df_years)

        # sunfig = go.Figure()
        self.sunfig.add_trace(go.Sunburst(
            labels=sun_trees['id'],
            parents=sun_trees['parent'],
            values=sun_trees['counts'],
            branchvalues='total',
            hovertemplate='<b>%{label} </b> <br> Sales: %{value}<br>',
            textinfo='label+value'
        ))

        self.sunfig.update_layout(margin=dict(t=10, l=10, r=10, b=10))
        return self.__figjson(self.sunfig)
    
            
    def plot_histogram(self, pheno='Whiteness_Degree_of_Complete_Grain(%)', height=600):
        fig = px.histogram(self.data[[pheno]], x=pheno, height=height,template="simple_white")
        fig.update_xaxes(tickfont=dict(size=16), title_font=dict(size=18))
        fig.update_yaxes(tickfont=dict(size=16), title_font=dict(size=18))
        return self.__figjson(fig)

    def plot_distr(self, height=800):
        distr = pd.DataFrame(self.pheno_stats, columns=['Counts']).sort_values(by=['Counts'])
        distr.index.name='Phenotype'
        fig = px.bar(distr.reset_index(), x='Counts',y='Phenotype', orientation='h', height=height)
        return self.__figjson(fig)

    def plot_pie(self, height=600):
        fig = go.Figure(data=[go.Pie(labels=self.labels, values=self.counts)])
        fig.update_layout(height=height)
        return self.__figjson(fig)
        
    def construct_table(self, pheno_name, species='rice', datatype='GVCF', suffix='raw.g.vcf.gz'):
        headers = ['Sample_ID', 'Name', pheno_name, 'Years', 'Region']
        pheno = self.data[headers].dropna(subset=[pheno_name])
        pheno['Download'] = pheno['Sample_ID'].apply(lambda x: self.ftp_temp.format(species=species, datatype=datatype, sampleid=x, suffix=suffix))
        return pheno
    
    def plot_heatmap(self, height=1200, width=1200):
        fig = px.imshow(self.pheno.corr(numeric_only=True),
            width=width,
            height=height, 
            color_continuous_scale='Blues')
        return self.__figjson(fig)

