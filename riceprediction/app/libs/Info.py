#!/usr/bin/env python3
# -*- coding=utf-8 -*-

'''
Author: shenzijie
Date: 2022-10-15 22:11:39
LastEditors: shenzijie
LastEditTime: 2023-06-10 23:49:41
Email: shenzijie2013@163.com
'''

import json, plotly
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class Info:
    '''read a file with csv form, return figure json'''  
    def __init__(self,csvfile):
        self.data = pd.read_csv(csvfile, header=0)
        self.pheno_values = self.data.iloc[:,4:41].copy()
        self.pheno_stats = self.pheno_values.count()
        self.labels = self.pheno_stats.index
        self.counts = self.pheno_stats.values
        self.ftp_temp = 'https://{spiece}/{datatype}/{sampleid}'
        self.table = ''

    def _figjson(self, fig):
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
    def plot_histogram(self, pheno='Whiteness_Degree_of_Complete_Grain(%)', height=600):
        fig = px.histogram(self.data[[pheno]], x=pheno, height=height)
        return self._figjson(fig)

    def plot_distr(self, height=800):
        distr = pd.DataFrame(self.pheno_stats, columns=['Counts']).sort_values(by=['Counts'])
        distr.index.name='Phenotype'
        fig = px.bar(distr.reset_index(), x='Counts',y='Phenotype', orientation='h', height=height)
        return self._figjson(fig)

    def plot_pie(self, height=600):
        fig = go.Figure(data=[go.Pie(labels=self.labels, values=self.counts)])
        fig.update_layout(height=height)
        return self._figjson(fig)
        
    def construct_table(self, pheno_name, spiece='rice', datatype='SNPs'):
        headers = ['Sample_ID', 'Name', pheno_name, 'Treatment','Years', 'Region']
        pheno = self.data[headers].dropna(subset=[pheno_name])
        pheno['Download'] = pheno['Sample_ID'].apply(lambda x: self.ftp_temp.format(spiece=spiece, datatype=datatype, sampleid=x))
        return pheno
        