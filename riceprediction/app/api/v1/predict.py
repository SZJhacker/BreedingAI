import os, joblib, pickle
import numpy as np
import pandas as pd
from flask import render_template, request, flash
from app.libs.redprint import Redprint
from app.validations.upload import UploadFile

api = Redprint('predict')

# gru_gw_path = os.path.join(os.path.dirname(__file__), 'static/model/gw_xie_liang_nc_nature.gru.pkl')
# gru_gl_path = os.path.join(os.path.dirname(__file__), 'static/model/gl_xie_liang_nc_nature.gru.pkl')
# cloned_gene = os.path.join(os.path.dirname(__file__), 'static/file/cloned.genes.overlap.csv')
# gru_gw_path = os.path.join(os.path.dirname(__file__), 'static/model/gw_xie_liang_nc_nature.gru.pkl')

# 归一化模型地址
pn_scaler_path = os.path.join(os.path.dirname(__file__), 'static/model/scaler/pn_alldata.rm0.lasso.10fold.scaler.joblib')
ph_scaler_path = os.path.join(os.path.dirname(__file__), 'static/model/scaler/ph_alldata.rm0.lasso.10fold.scaler.joblib')
gl_scaler_path = os.path.join(os.path.dirname(__file__), 'static/model/scaler/gl_alldata.rm0.lasso.10fold.scaler.joblib')
gw_scaler_path = os.path.join(os.path.dirname(__file__), 'static/model/scaler/gw_alldata.rm0.lasso.10fold.scaler.joblib')

# 预测模型地址
gru_pn_path = os.path.join(os.path.dirname(__file__), 'static/model/pn_alldata.rm0.lasso.10fold2.gru.r2.joblib')
gru_ph_path = os.path.join(os.path.dirname(__file__), 'static/model/ph_alldata.rm0.lasso.10fold2.gru.r2.joblib')
gru_gl_path = os.path.join(os.path.dirname(__file__), 'static/model/gl_alldata.rm0.lasso.10fold7.gru.r2.joblib')
gru_gw_path = os.path.join(os.path.dirname(__file__), 'static/model/gw_alldata.rm0.lasso.10fold3.gru.r2.joblib')

# 导入lasso选择的基因
pheno_path = os.path.join(os.path.dirname(__file__), 'static/file/rm0.lasso.4pheno.pkl')

def reshape_for_gru(data):
    return np.reshape(data, (data.shape[0], 1, -1)).astype(np.float32)

@api.route('/', methods=['POST','GET'])
def predict():
    fileform = UploadFile()
    if request.method == 'POST' and fileform.validate_on_submit():
        with open(pheno_path, 'rb') as f:
            phenos = pickle.load(f)
        # headers = pd.read_csv(cloned_gene)
        try:
            features_file = pd.read_csv(fileform.file.data, index_col='sample')
            samples = features_file.index.tolist() # 文件名称
            # features = features_file[headers['0'].values.tolist()].values
            # features = features.reshape(-1, 1, features.shape[1]).astype(np.float32)

            # 导入归一化模型
            pn_scaler = joblib.load(pn_scaler_path)
            ph_scaler = joblib.load(ph_scaler_path)
            gl_scaler = joblib.load(gl_scaler_path)
            gw_scaler = joblib.load(gw_scaler_path)

            pn_model = joblib.load(gru_pn_path)
            ph_model = joblib.load(gru_ph_path)
            gl_model = joblib.load(gru_gl_path)
            gw_model = joblib.load(gru_gw_path)


            # 特征选择
            pn_features = features_file[phenos['panicle number']].values
            ph_features = features_file[phenos['plant height']].values
            gl_features = features_file[phenos['grain length']].values
            gw_features = features_file[phenos['grain witdh']].values

            # 上传数据归一化
            pn_features_scaler = reshape_for_gru(pn_scaler.transform(pn_features))
            ph_features_scaler = reshape_for_gru(ph_scaler.transform(ph_features))
            gl_features_scaler = reshape_for_gru(gl_scaler.transform(gl_features))
            gw_features_scaler = reshape_for_gru(gw_scaler.transform(gw_features))

            pn_result = pn_model.predict(pn_features_scaler)
            ph_result = ph_model.predict(ph_features_scaler)
            gl_result = gl_model.predict(gl_features_scaler)
            gw_result = gw_model.predict(gw_features_scaler)
            # result_data = [{'sample': sample, 'gw': gw, 'gl': gl} for sample, gw, gl in zip(samples, gw_result, gl_result)]
            result_data = [{'sample': sample, 'pn': pn, 'ph':ph, 'gl': gl, 'gw':gw} for sample, pn, ph, gl, gw in zip(samples, pn_result, ph_result, gl_result, gw_result)]
            return render_template('predict_result.html', result_data=result_data)
        except Exception as e:
            if "sample" in str(e):
                flash("Your data may not have 'sample' header specifying the sample name.", 'error')
            elif "not in index" in str(e):
                flash("Your data may be not gsctool features.", 'error')
            else:
            # 其他异常情况
                flash(f"Error: {str(e)}", "error")
    return render_template('predict.html', form=fileform)
