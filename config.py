#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""
Default config for xponentialy
"""
import string

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

# Mail
MAIL_DEFAULT_SENDER = 'no-reply@demo.xponentialy.com'

# Security
SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
SECURITY_URL_PREFIX = '/auth'

AUTH_PASSWD_LEN = 8
AUTH_PASSWD_ALPHABET = string.letters + string.digits