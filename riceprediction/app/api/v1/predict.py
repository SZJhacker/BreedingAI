import os, joblib
import pandas as pd
from flask import render_template, request
from app.libs.redprint import Redprint
from app.validations.upload import UploadForm

api = Redprint('predict')

gru_gw_path = os.path.join(os.path.dirname(__file__), 'file/gw_xie_liang_nc_nature.gru.pkl')
gru_gl_path = os.path.join(os.path.dirname(__file__), 'file/gl_xie_liang_nc_nature.gru.pkl')

@api.route('/', methods=['POST','GET'])
def predict():
    fileform = UploadForm()
    if request.method == 'POST' and fileform.validate_on_submit():
        features = pd.read_csv(fileform.file.data)
        gw_model = joblib.load(gru_gw_path)  # 加载训练好的模型
        gl_model = joblib.load(gru_gl_path)
    return render_template('predict.html', form=fileform)
