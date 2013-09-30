#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""

"""
from flask.ext.admin.contrib.sqlamodel import ModelView
from sqlalchemy.ext.declarative import DeclarativeMeta


def create_views(admin_manager, db):
    """
    Create API endpoints using a bounded instance of
    :class:`flask.ext.admin.Admin`.
    """
    from xponentialy import models
    for i in models.__dict__.values():
        if isinstance(i, DeclarativeMeta):
            admin_manager.add_view(ModelView(i, db.session))
