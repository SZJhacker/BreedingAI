from flask import render_template
from app.libs.redprint import Redprint

api = Redprint('about_cn')

@api.route('/', endpoint='about_cn')
def about():
    return render_template('about_cn.html')