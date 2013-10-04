#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""

"""
__version__ = '0.2.0a1'
from flask import Flask


def config_app():
    app = Flask(__name__)
    app.config.from_object('config')
    try:
        # try load deployment config
        app.config.from_envvar('DEPLOYMENT_CONFIG')
    except RuntimeError:
        import os
        app.logger.warning(
            'Cannot load DEPLOYMENT_CONFIG, ignore; os.environ: %s',
            os.environ)
    from models import db
    db.init_app(app)
    return app, db


def create_db_manager():
    app, db = config_app()
    from flask.ext.script import Manager
    from flask.ext.migrate import Migrate, MigrateCommand
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    return manager


def create_app():
    app, db = config_app()

    from flask.ext.restless import APIManager
    from flask.ext.admin import Admin
    from xponentialy import views

    api = APIManager(app, flask_sqlalchemy_db=db)
    views.api.create_views(api)

    admin = Admin(app)
    views.admin.create_views(admin, db)

    app.register_blueprint(views.fitbit.fitbit_bp, url_prefix='/fitbit')

    return app
