#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os,time
from flask import render_template, current_app, send_file, after_this_request
from app.libs.redprint import Redprint
from app.libs.gsctool import GenomeFeature
from app.validations.upload import UploadFilegz

api = Redprint('ML')

gff_path_dir = os.path.join(os.path.dirname(__file__), 'static/file')

def generate_name(spiece):
    timestamp = int(time.time())
    tmp = os.path.join(os.path.dirname(__file__), 'static/tmp', f'{spiece}.{timestamp}.csv')
    return tmp

@api.route('/features', endpoint='features', methods=['GET', 'POST'])
def features():
    form = UploadFilegz()
    if form.validate_on_submit():
        vcffile = form.file.data
        species = form.species.data
        filename = generate_name(species)
        gff_path = {'rice': os.path.join(gff_path_dir,"IRGSP-1.0_representative_2023-03-15.tar.gz"),
                    'zea' : os.path.join(gff_path_dir,'Zea_mays.Zm-B73-REFERENCE-NAM-5.0.56.gff3.gz'),
                    'soy' : os.path.join(gff_path_dir,'Glycine_max.Glycine_max_v2.1.56.gff3.gz')}
        features = GenomeFeature(gff_path[species], vcffile)
        outfile = features.parse()
        outfile.to_csv(filename)
        @after_this_request
        def remove_file(response):
            # 删除文件
            os.remove(filename)
            return response
        return send_file(
            filename,
            mimetype='text/csv',
            as_attachment=True
        )
    return render_template('features.html', form=form)