#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :prediction.py
@说明        :
@时间        :2021/01/13 11:05:20
'''

import optuna, json, plotly
import numpy as np
import pandas as pd
import plotly.express as px
from lightgbm import LGBMRegressor
from flask import render_template, request
from app.libs.redprint import Redprint
from app.validations.lgbPara import SearchSpace

api = Redprint('prediction')

def figjson(fig):
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def get_k_fold_data(k, i, X, y):
    assert k > 1
    fold_size = X.shape[0] // k
    X_train, y_train = None, None
    for j in range(k):
        idx = slice(j * fold_size, (j + 1) * fold_size)
        X_part, y_part = X[idx, :], y[idx]
        if j == i:
            X_valid, y_valid = X_part, y_part
        elif X_train is None:
            X_train, y_train = X_part, y_part
        else:
            X_train = np.concatenate([X_train, X_part], 0)
            y_train = np.concatenate([y_train, y_part], 0)
    return X_train, y_train, X_valid, y_valid


@api.route('/', methods=['GET', 'POST'])
def prediction():
    search_space = SearchSpace()
    if request.method == "POST" and search_space.validate_on_submit():
        features = pd.read_csv(search_space.features.data, header=0)
        X, y = features.iloc[:, :-1], features.iloc[:, -1]
        x_train, y_train, x_valid, y_valid = get_k_fold_data(5, 1, X.values, y.values)
        optuna.logging.set_verbosity(optuna.logging.WARNING) # 压缩报告信息
        study_tuner = optuna.create_study(direction='maxmize', pruner=optuna.pruners.MedianPruner())
        kwargs=search_space
        def objective(trial):
            param = {
                'metric': kwargs.metric.data.strip(), 
                "boosting_type": kwargs.boosting_type.data.strip(),                
                "seed": kwargs.seed.data,
                "verbosity": -1,
                "n_estimators": trial.suggest_int('n_estimators', kwargs.n_estimators_min.data, kwargs.n_estimators_max.data),
                "learning_rate": trial.suggest_float("learning_rate", kwargs.learning_rate_min.data, kwargs.learning_rate_max.data),
                "max_depth": trial.suggest_int("max_depth", kwargs.max_depth_min.data, kwargs.max_depth_max.data),
                'num_leaves': trial.suggest_int('num_leaves', kwargs.leaves_min.data, kwargs.leaves_max.data),
                'min_child_samples': trial.suggest_int('min_child_samples', kwargs.min_child_min.data, kwargs.min_child_max.data),
                'feature_fraction': trial.suggest_uniform('feature_fraction', kwargs.features_fraction_min.data, kwargs.features_fraction_max.data),
                'bagging_fraction': trial.suggest_uniform('bagging_fraction', kwargs.bagging_fraction_min.data, kwargs.bagging_fraction_max.data),
                'lambda_l1': trial.suggest_loguniform('lambda_l1', kwargs.lambda_l1_min.data, kwargs.lambda_l1_max.data),
                'lambda_l2': trial.suggest_loguniform('lambda_l2', kwargs.lambda_l2_min.data, kwargs.lambda_l2_max.data),
            }
            lgb=LGBMRegressor(**param)
            pruning_callback = optuna.integration.LightGBMPruningCallback(trial, "l2")
            lgb.fit(x_train, y_train, eval_set=[(x_valid, y_valid)],callbacks=[pruning_callback])
            return lgb.score(x_valid, y_valid)
        study_tuner.optimize(objective, n_trials=search_space.trails.data)

        fig_history = figjson(optuna.visualization.plot_optimization_history(study_tuner))
        fig_para = figjson(optuna.visualization.plot_param_importances(study_tuner))

        lgb = LGBMRegressor(**study_tuner.best_params)
        lgb.fit(x_train, y_train, eval_set=[(x_valid, y_valid)])
        feature_importance = pd.DataFrame(lgb.feature_importances_,
                                            index=X.columns.values,
                                            columns=['feature_importance']).sort_values('feature_importance').tail(10)
        fig_features = figjson(px.bar(feature_importance, orientation='h', height=400))
        print('分析完成')
        return render_template('predict_results.html', graphJSON_history=fig_history, graphJSON_paras=fig_para, graphJSON_features=fig_features)
    return render_template('prediction.html', space=search_space)

