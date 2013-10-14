#!/usr/env/bin python
# -*- coding: utf-8 -*-
from flask.ext.peewee.auth import Auth
from flask.ext.peewee.admin import Admin, ModelAdmin

from xponentialy import app, db
from xponentialy import models

auth = Auth(app, db)
admin = Admin(app, auth)


class UserAdmin(ModelAdmin):
    exclude = ['password']

admin.register(models.User, UserAdmin)
registered = ['User']
for name in models.__all__:
    if name not in registered:
        admin.register(getattr(models, name))


admin.setup()