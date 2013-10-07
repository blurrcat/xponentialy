#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""
Default config for xponentialy
"""

DEBUG = True

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://root:root@127.0.0.1:3306/xponentialy_dev')
SQLALCHEMY_ECHO = True

SECRET_KEY = '\x03\xea\xd2`\x9a8P\x86>\xf4 \xfe3br^e\xbfw\xf1'

# Fitbit
FITBIT_KEY = ''
FITBIT_SECRET = ''
SUBSCRIPTION_COLLECTION = None
SUBSCRIPTION_ID = ''

# Tasks
TASK_RETRY_INTERVAL = 30
TASK_RETRY_MAX = 3