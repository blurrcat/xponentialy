#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""

"""
from flask import Flask



def _create_app(config_file):
    app = Flask(__name__)
    app.config.from_object(config_file)
    try:
        app.config.from_envvar('FLASK_EB_CONFIG')  # try load production config
    except RuntimeError:
        pass
    return app


def create_db_manager(config_file='config'):
    app = _create_app(config_file)
    from models import db
    db.init_app(app)
    from flask.ext.script import Manager
    from flask.ext.migrate import Migrate, MigrateCommand
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    return manager




def create_app(config_file='config'):
    app = _create_app(config_file)

    from models import db
    db.init_app(app)

    from flask.ext.restless import APIManager
    from flask.ext.admin import Admin
    from xponentialy import views

    api = APIManager(app)
    views.api.create_views(api)

    admin = Admin(app)
    views.admin.create_views(admin, db)

    return app


if __name__ == '__main__':
    create_database('config')