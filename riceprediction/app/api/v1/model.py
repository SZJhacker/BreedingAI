#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :prediction.py
@说明        :
@时间        :2021/01/13 11:05:20
'''

import os, optuna, json, plotly, joblib, time
import numpy as np
import pandas as pd
# import plotly.express as px
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error
from flask import render_template, request, after_this_request, send_file, flash
from app.libs.redprint import Redprint
from app.validations.lgbPara import SearchSpace

api = Redprint('model')


def generate_name():
    timestamp = int(time.time())
    pkl = os.path.join(os.path.dirname(__file__), 'static/tmp', f'lgb.{timestamp}.joblib')
    return pkl

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
def model():
    search_space = SearchSpace()
    if request.method == "POST" and search_space.validate_on_submit():
        # 读取 CSV 文件，指定 'sample' 列为索引列
        try:
            features = pd.read_csv(search_space.features.data, index_col='sample')

            # 获取特征列和标签列
            X = features.drop(columns=['labels'])  # 剩余的列为特征列
            y = features['labels']  # 'label' 列为标签列
            x_train, y_train, x_valid, y_valid = get_k_fold_data(5, 1, X.values, y.values)
            kwargs = search_space

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
                pruning_callback = optuna.integration.LightGBMPruningCallback(trial, 'l2')
                lgb.fit(x_train, y_train, eval_set=[(x_valid, y_valid)],callbacks=[pruning_callback])
                preds = lgb.predict(x_valid)
                accuracy = np.sqrt(mean_squared_error(y_valid, preds))
                return accuracy
            

            optuna.logging.set_verbosity(optuna.logging.WARNING) # 压缩报告信息
            study_tuner = optuna.create_study(direction='minimize', pruner=optuna.pruners.MedianPruner())
            study_tuner.optimize(objective, n_trials=search_space.trails.data)

            # 绘制optuna训练历史
            # fig_history = figjson(optuna.visualization.plot_optimization_history(study_tuner))
            # fig_para = figjson(optuna.visualization.plot_param_importances(study_tuner))

            lgb = LGBMRegressor(**study_tuner.best_params)
            lgb.fit(x_train, y_train, eval_set=[(x_valid, y_valid)])

            ## 绘制最有模型中的重要特征
            # feature_importance = pd.DataFrame(lgb.feature_importances_,
            #                                     index=X.columns.values,
            #                                     columns=['feature_importance']).sort_values('feature_importance').tail(10)
            # fig_features = figjson(px.bar(feature_importance, orientation='h', height=400))
            # return render_template('predict_results.html', graphJSON_history=fig_history, graphJSON_paras=fig_para, graphJSON_features=fig_features)

            
            # 最优模型返回
            filename = generate_name()
            joblib.dump(lgb, filename)
            @after_this_request
            def remove_file(response):
                os.remove(filename)
                return response
            return send_file(
                filename,
                mimetype='application/octet-stream',
                as_attachment=True
            )
        except Exception as e:
            if "sample" in str(e):
                flash("Your data may not have 'sample' header specifying the sample name.", 'error')
            else:
            # 其他异常情况
                flash(f"Error: {str(e)}", "error")

    return render_template('model.html', space=search_space)

