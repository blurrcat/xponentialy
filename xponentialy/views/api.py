#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""

"""
from sqlalchemy.ext.declarative import DeclarativeMeta


def create_views(api_manager):
    """
    Create API endpoints using a bounded instance of
    :class:`flask.ext.restless.APIManager`.
    """
    from xponentialy import models
    for i in models.__dict__.values():
        if isinstance(i, DeclarativeMeta):
            api_manager.create_api(i, methods=['GET', 'POST', 'PUT'])