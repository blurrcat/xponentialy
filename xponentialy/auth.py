# #!/usr/env/bin python
# # -*- coding: utf-8 -*-
import functools

from flask import g, Response, abort
from flask import session
from flask.ext.peewee.auth import Auth

from xponentialy import app, db
from xponentialy.models import User


class XpAuth(Auth):

    def login_user(self, user):
        super(XpAuth, self).login_user(user)
        try:
            u = User.select(User.company).where(User.id == user.id).get()
        except User.DoesNotExist:
            pass
        else:
            if u.company:
                session['company_pk'] = u.company.id
                g.company = u.company

    def get_current_company_id(self):
        if session.get('logged_in'):
            try:
                return session.get('company_pk')
            except KeyError:
                abort(404)

    def test_user_or_401(self, test_fn):
        """
        Test if the user is currently logged in. If not, return 401
        """
        def decorator(fn):
            @functools.wraps(fn)
            def inner(*args, **kwargs):
                user = self.get_logged_in_user()
                if not user or not test_fn(user):
                    return Response('Authentication failed', 401)
                return fn(*args, **kwargs)
            return inner
        return decorator

    def logged_in_or_401(self, func):
        return self.test_user_or_401(lambda u: True)(func)


auth = XpAuth(app, db)



# import random
#
# from flask import request
# from flask import current_app
# from flask.ext.security import SQLAlchemyUserDatastore, Security
# from flask.ext.security import login_required
# from xponentialy.models import User, Role
#
# security = Security()
#
#
# def _gen_password():
#     conf = current_app.config
#     return ''.join(random.choice(
#         conf['AUTH_PASSWD_ALPHABET']) for _ in xrange(conf['AUTH_PASSWD_LEN']))
#
#
# @login_required
# def user_info():
#     if request.method == 'GET':
#         return 'user info form; must reset password'
#     else:
#         return 'process form'
#
#
# def create_views(app, db):
#     user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#     security.init_app(app, datastore=user_datastore)
#     app.add_url_rule('/auth/user_info', view_func=user_info,
#                      methods=['GET', 'POST'])