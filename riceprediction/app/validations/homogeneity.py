#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, FileField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Email


class MySelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        """overrides post validation"""
        # Here is my custom validation
        pass

class MyFileField(FileField):
    """为vcf.gz文件创建索引，根据任务是否执行成功返回布尔值"""
    def create_index(self, filepath):
        print(f'tabix -p vcf {filepath}')
        return bool(not os.system(f'tabix -p vcf {filepath}')) 


class EmailForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[Email(message="Inavailable Email Address"),
                    DataRequired(message="The email is required for receiving the result")],
        description="We'll never share your email with anyone else.")

class HomogeneSearch(EmailForm):
    # rice = MySelectMultipleField(u'source', choices=[], coerce=str)
    # target_rice = MySelectMultipleField(u'target', choices=[])
    attach = MyFileField(
        u'Vcf.gz Attachment',
        validators=[FileRequired(),
                    FileAllowed(['vcf.gz'], 'vcf.gz only!')])
    submit = SubmitField('Submit')

class HomogeneComp(HomogeneSearch):
    rice_single = SelectField(u'Please select the Variety which you want to compared with', choices=[], coerce=str, validate_choice=False, validators=[DataRequired("Please select the variety")])

    def rice_info(self, field):
        """填充水稻的品种信息"""
        self.rice_single.choices = [(rice.assay, rice.accession) for rice in field]


class EmailFormCN(FlaskForm):
    email = StringField(
        u'邮箱地址',
        validators=[Email(message='邮箱格式不正确'), DataRequired(message="该邮箱用于接受分析结果")],
        description="我们不会将你的邮箱分享给任何人.")


class HomogeneSearchCN(EmailFormCN):
    # Text Field类型，文本输入框，Email格式
    # rice = MySelectMultipleField(u'source', choices=[], coerce=str)
    # target_rice = MySelectMultipleField(u'target', choices=[])
    attach = MyFileField(
        u'请上传您的vcf.gz文件（bzip压缩）',
        validators=[FileRequired(),
                    FileAllowed(['vcf.gz'], '仅允许vcf.gz文件上传!')])
    submit = SubmitField('提交')

class HomogeneCompCN(HomogeneSearchCN):
    rice_single = SelectField(u'请选择你需要进行比较的品种', choices=[], coerce=str, validate_choice=False, validators=[DataRequired("请选择要比较的品种")])

    def rice_info(self, field):
        """填充水稻的品种信息"""
        self.rice_single.choices = [(rice.assay, rice.accession) for rice in field]
    


