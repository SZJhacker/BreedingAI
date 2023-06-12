#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileSize
from wtforms import  SubmitField, FileField, RadioField

class UploadFile(FlaskForm):
    file = FileField(
        'Please upload a gzip-compressed VCF file with a maximum file size of 100MB.',
        validators=[FileRequired(),
                    FileAllowed(['gz'], 'Gzip-compressed Files Only!'),
                    FileSize(max_size=100 * 1024 * 1024, message='File size should be less than 100 MB')])
    spieces = RadioField('Spiece', 
                         choices=[('rice','rice'),
                                  ('soybean', 'soy'),
                                  ('zea','zea')], 
                        default='rice')
    submit = SubmitField('Submit')