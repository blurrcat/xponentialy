#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Harry Liang <blurrcat@gmail.com>
"""

"""
from xponentialy import load_app
from flask.ext.script import Manager, prompt, prompt_pass, prompt_bool
from flask.ext.script.commands import ShowUrls


manager = Manager(load_app)
db = Manager(usage='Database housekeepings. See sub-commands.')
auth = Manager(usage='User management')


@db.command
def create_all():
    """Create all tables defined in xponentialy.models in current database."""
    from xponentialy import models
    for name in models.__all__:
        model = getattr(models, name)
        model.create_table(fail_silently=True)
        print 'Created table for %s' % name
    print 'All tables created.'


@auth.command
def create_user():
    """
    Create a user
    """
    import re
    import sys
    from xponentialy.models import User
    from flask.ext.peewee.utils import make_password
    email = prompt('Email')
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                    email):
        print 'Error: Invalid email address'
        sys.exit(-1)
    name = email.split('@')[0]
    name = prompt('Username', default=name)
    passwd = prompt_pass('Password')
    passwd2 = prompt_pass('Password again')
    if passwd2 != passwd:
        print 'Error: Password not match'
        sys.exit(-1)
    admin = prompt_bool('Is Admin?', default=False)
    User.create(username=name, password=make_password(passwd), email=email,
                admin=admin, active=True)
    print 'User created.'


manager.add_command('db', db)
manager.add_command('accounts', auth)
manager.add_command('urls', ShowUrls())
manager.run()