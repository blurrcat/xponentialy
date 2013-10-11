#!/usr/env/bin python
# -*- coding: utf-8 -*-
import random

from flask import request
from flask import current_app
from flask.ext.security import SQLAlchemyUserDatastore, Security
from flask.ext.security import login_required
from xponentialy.models import User, Role

security = Security()


def _gen_password():
    conf = current_app.config
    return ''.join(random.choice(
        conf['AUTH_PASSWD_ALPHABET']) for _ in xrange(conf['AUTH_PASSWD_LEN']))


@login_required
def user_info():
    if request.method == 'GET':
        return 'user info form; must reset password'
    else:
        return 'process form'


def create_views(app, db):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=user_datastore)
    app.add_url_rule('/auth/user_info', view_func=user_info,
                     methods=['GET', 'POST'])