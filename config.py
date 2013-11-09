#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""
Default config for xponentialy
"""
import logging

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
FITBIT_SUBSCRIPTION_COLLECTIONS = ['sleep', 'activities']
FITBIT_SUBSCRIPTION_ID = 'ec2-dev'
# how long to sync data when the user first connects to us
FITBIT_SYNC_DAYS = 30
FITBIT_INTRADAY_ENABLED = False
FITBIT_INTRADAY_DETAIL_LEVEL = '1min'
FITBIT_INTRADAY_RESOURCES = ('steps', 'distance', 'calories', 'floors',
                             'elevation')

# Tasks
TASK_RETRY_INTERVAL = 30
TASK_RETRY_MAX = 3

# Mail
MAIL_SERVER = 'localhost'

# API
API_VERSION = 1

# Logging
LOG_FILE = '/tmp/xponentialy.log'
LOG_MAX_BYTES = 10485760  # 10MB
LOG_BACKUP_COUNT = 10
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
