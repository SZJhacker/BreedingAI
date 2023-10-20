import os, joblib
import numpy as np
import pandas as pd
from flask import render_template, request, url_for
from app.libs.redprint import Redprint
from app.validations.upload import UploadFile

api = Redprint('predict')

gru_gw_path = os.path.join(os.path.dirname(__file__), 'static/model/gw_xie_liang_nc_nature.gru.pkl')
gru_gl_path = os.path.join(os.path.dirname(__file__), 'static/model/gl_xie_liang_nc_nature.gru.pkl')
cloned_gene = os.path.join(os.path.dirname(__file__), 'static/file/cloned.genes.overlap.csv')

@api.route('/', methods=['POST','GET'])
def predict():
    fileform = UploadFile()
    if request.method == 'POST' and fileform.validate_on_submit():
        print('完成提交')
        headers = pd.read_csv(cloned_gene)
        features = pd.read_csv(fileform.file.data, usecols=headers['0'].values.tolist()).values
        features = features.reshape(-1, 1, features.shape[1]).astype(np.float32)
        gw_model = joblib.load(gru_gw_path)  # 加载训练好的模型
        gl_model = joblib.load(gru_gl_path)
        gw_result = gw_model.predict(features)
        gl_result = gl_model.predict(features)
        result_data = [{'gw': gw, 'gl': gl} for gw, gl in zip(gw_result, gl_result)]
        return render_template('predict_result.html', result_data=result_data)
    return render_template('predict.html', form=fileform)
