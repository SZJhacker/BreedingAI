#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :__init__.py
@说明        :
@时间        :2020/12/21 13:08:38
'''

from flask import Flask
from flask_bootstrap import Bootstrap4
from app.libs.email import mail

def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/BreedingAI/')

def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap4()
    app.config.from_pyfile('setting.py')
    app.config.from_pyfile('secure.py')

    register_blueprints(app)
    register_plugin(app)
    bootstrap.init_app(app)
    mail.init_app(app)

    return app