#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""

"""
from flask.ext.peewee.admin import Admin, ModelAdmin

from xponentialy import app
from xponentialy import models
from xponentialy.auth import auth


admin = Admin(app, auth, branding='Xponentialy Admin')


class UserAdmin(ModelAdmin):
    exclude = ['password']

admin.register(models.User, UserAdmin)
registered = ['User']
for name in models.__all__:
    if name not in registered:
        admin.register(getattr(models, name))


admin.setup()