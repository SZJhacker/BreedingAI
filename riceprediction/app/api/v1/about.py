from flask import render_template
from app.libs.redprint import Redprint

api = Redprint('about')

@api.route('/')
def about():
    return render_template('about.html')