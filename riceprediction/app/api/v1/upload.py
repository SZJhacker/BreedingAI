#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app.libs.redprint import Redprint
from app.validations.upload import UploadForm
from app.validations.info import InfoForm
from app.models.uploadata import UploadedData
from app.models.info import Info
from app.models.base import db
api = Redprint('uplaod')


@api.route('/', methods=['GET', 'POST'])
def upload():
    fileform = UploadForm()
    info = InfoForm()

    if request.method == 'POST':
        if fileform.validate_on_submit():
            # 获取表单数据
            phenotype = fileform.phenotype.data
            specie = fileform.species.data
            reference_genome = fileform.reference_genome.data
            planting_region = fileform.planting_region.data
            planting_year = fileform.planting_year.data
            file = fileform.file.data

            # 保存文件到服务器
            filename = file.filename
            file.save('uploads/' + filename)

            # 将上传的数据保存到数据库
            data = UploadedData(phenotype, specie, reference_genome, planting_region, planting_year, filename)
            data.save()

            flash('File uploaded successfully! Thank you.', 'success')
        else:
            info = Info(
                article=info.article.data,
                bioproject=info.bioproject.data,
                specie=info.specie.data
                # 设置其他字段的值
            )
            info.save()
            flash('Info submitted successfully! Thank you.', 'success')
        return redirect(url_for('v1.upload'))

    return render_template('upload.html', fileform=fileform, infoform=info)

