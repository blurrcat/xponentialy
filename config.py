#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""
Default config for xponentialy
"""

DEBUG = True

# Database
DATABASE = {
    'name': 'xponentialy_peewee',
    'engine': 'peewee.MySQLDatabase',
    'user': 'root',
    'passwd': 'root',
    'threadlocals': True,
}

SECRET_KEY = '\x03\xea\xd2`\x9a8P\x86>\xf4 \xfe3br^e\xbfw\xf1'

# Fitbit
FITBIT_KEY = ''
FITBIT_SECRET = ''
FITBIT_OAUTH = {
    'base_url': 'https://api.fitbit.com',
    'request_token_url': 'http://api.fitbit.com/oauth/request_token',
    'access_token_url': 'http://api.fitbit.com/oauth/access_token',
    'authorize_url': 'http://www.fitbit.com/oauth/authorize',
}
FITBIT_SUBSCRIPTION_COLLECTIONS = ['activities']
FITBIT_SUBSCRIPTION_ID = 'ec2-dev'

# Tasks
TASK_RETRY_INTERVAL = 30
TASK_RETRY_MAX = 3

# Mail
MAIL_SERVER = 'localhost'

# API
API_VERSION = 1

# Security
SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
SECURITY_EMAIL_SENDER = 'no-reply@demo.xponential.ly'
SECURITY_URL_PREFIX = '/auth'
SECURITY_POST_CONFIRM_VIEW = '/fitbit/confirmed'
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = '___stupid_dev_salt__'
