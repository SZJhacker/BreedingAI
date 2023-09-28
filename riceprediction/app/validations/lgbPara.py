#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import RadioField, IntegerField, SubmitField, FileField, FloatField
from wtforms.validators import NumberRange, DataRequired


class SearchSpace(FlaskForm):
    boosting_type = RadioField(
        'Boosting Type',
        choices=[('gbdt', 'gbdt'),
                 ('Random Forest', 'rf'),
                 ('Dropouts meet Multiple Additive Regression Trees', 'dart'),
                 ('Gradient-based One-Side Sampling', 'goss')],
        default='gbdt')
    metric = RadioField('Metrics',
                        choices=[('mse', 'mse'),
                                 ('mae', 'mae'),
                                 ('rmse', 'rmse'),
                                 ('rmsle', 'rmsle'), ('mape', 'mape'),
                                 ('smape', 'smape'), ('rmspe', 'rmspe')],
                        default='mse')
    n_estimators_min = IntegerField("N_estimators_min", default=100)
    n_estimators_max = IntegerField("N_estimators_max", default=1000)
    learning_rate_min = FloatField("learning_rate_min", default=0.01)
    learning_rate_max = FloatField("learning_rate_max", default=0.03)
    max_depth_min = IntegerField("max_depth_min", default=3)
    max_depth_max = FloatField("max_depth_max", default=12)
    leaves_min = IntegerField("leaves_min", default=2)
    leaves_max = IntegerField("leaves_max", default=256)
    min_child_min = IntegerField("min_child_min", default=10)
    min_child_max = IntegerField("min_child_max", default=100)
    features_fraction_min = FloatField('features_fraction_min', default=0.1)
    features_fraction_max = FloatField('features_fraction_max', default=1.0)
    bagging_fraction_min = FloatField('bagging_fraction_min', default=0.1)
    bagging_fraction_max = FloatField('bagging_fraction_max', default=1.0)
    lambda_l1_min = FloatField('lambda_l1_min', default=1e-8)
    lambda_l1_max = FloatField('lambda_l1_max', default=10.0)
    lambda_l2_min = FloatField('lambda_l2_min', default=1e-8)
    lambda_l2_max = FloatField('lambda_l2_max', default=10.0)
    trails = IntegerField("Trails",
                          validators=[NumberRange(1, 200)],
                          default=20,
                          description='Number of trials to run')
    seed = IntegerField('Seed',
                        default=42,
                        description="Random state parameter")
    features = FileField(
        'Features',
        validators=[DataRequired()],
        description=
        "The features vectors of your crop genomen, whose last column is assigned the labels, please upload the file with csv or tsv format"
    )
    submit = SubmitField('Submit')