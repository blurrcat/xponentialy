#!/usr/env/bin python
# -*- coding: utf-8 -*-
import random

from flask import request
from flask import current_app
from flask.ext.security import SQLAlchemyUserDatastore, Security
from xponentialy.models import User, Role

security = Security()


def confirm():
    return 'hi'


def _gen_password():
    conf = current_app.config
    return ''.join(random.choice(
        conf['AUTH_PASSWD_ALPHABET']) for _ in xrange(conf['AUTH_PASSWD_LEN']))


def create_views(app, db):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=user_datastore)
    app.add_url_rule('/auth/confirm2', view_func=confirm)