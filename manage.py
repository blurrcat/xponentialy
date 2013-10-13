#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Harry Liang <blurrcat@gmail.com>
"""

"""
from xponentialy import load_app
from flask.ext.script import Manager, prompt_bool


manager = Manager(load_app)
db = Manager(usage="Database housekeepings. See sub-commands.")


@db.command
def drop_all():
    """Drop all tables defined in xponentialy.models from current database."""
    if prompt_bool('Are you sure to drop all tables?'):
        from peewee import BaseModel
        from xponentialy import models
        for item in dir(models):
            cls = getattr(models, item)
            if isinstance(cls, BaseModel):
                cls.drop_table(fail_silently=True)
        print 'All tables dropped.'


@db.command
def create_all():
    """Create all tables defined in xponentialy.models in current database."""
    from xponentialy import models
    order = [
        'House', 'User', 'Role', 'RolesUsers', 'Company', 'Survey', 'Activity',
        'IntradayActivity', 'Sleep', 'Update', 'Badge', 'UserBadge',
        'ForumThread', 'Challenge', 'ChallengeParticipant', 'InvalidPeriod',
        'Notification', 'Postsubscription', 'Emailmessage', 'Threadpost'
    ]
    for modelname in order:
        model = getattr(models, modelname)
        model.create_table(fail_silently=True)
    print 'All tables created.'


manager.add_command('db', db)
manager.run()