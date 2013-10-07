#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Harry Liang <blurrcat@gmail.com>
"""

"""
from . import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.INTEGER(display_width=11),
                   primary_key=True, nullable=False)
    first_name = db.Column(db.VARCHAR(length=20))
    last_name = db.Column(db.VARCHAR(length=20))
    fitbit_id = db.Column(db.VARCHAR(length=10), nullable=False)
    oauth_token = db.Column(db.VARCHAR(length=40), nullable=False)
    oauth_secret = db.Column(db.VARCHAR(length=40), nullable=False)
    profile_pic = db.Column(db.VARCHAR(length=200), nullable=False)
    gender = db.Column(db.VARCHAR(length=10), nullable=False)
    house_id = db.Column(db.INTEGER(display_width=11),
                         db.ForeignKey('house.id'))
    company_id = db.Column(db.INTEGER, db.ForeignKey('company.id'))
    username = db.Column(db.VARCHAR(length=20), nullable=False)
    email = db.Column(db.VARCHAR(length=40))
    admin = db.Column(db.BOOLEAN, nullable=False)
    phantom = db.Column(db.BOOLEAN, nullable=False)
    staff = db.Column(db.BOOLEAN, nullable=False)
    leader = db.Column(db.BOOLEAN, nullable=False)
    points = db.Column(db.INTEGER(display_width=11))
    fb = db.Column(db.BOOLEAN, nullable=False)
    badge_email_unsub = db.Column(db.BOOLEAN, nullable=False)
    daily_email_unsub = db.Column(db.BOOLEAN, nullable=False)
    challenge_email_unsub = db.Column(db.BOOLEAN, nullable=False)
    hide_progress = db.Column(db.BOOLEAN, nullable=False)

    def __unicode__(self):
        return u'[%s]%s' % (self.id, self.username)


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(length=128), nullable=False)
    description = db.Column(db.String(length=255))
    profile_pic = db.Column(db.VARCHAR(length=200), nullable=False)
    employees = db.relationship(User, backref='company')

    def __unicode__(self):
        return u'[%s]%s' % (self.id, self.name)


class Survey(db.Model):
    __tablename__ = 'survey'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER(display_width=11),
                        db.ForeignKey('user.id'), nullable=False)
    user = db.relation('User', uselist=False, backref='survey')
    q0 = db.Column(db.VARCHAR(length=1))
    q1 = db.Column(db.VARCHAR(length=1))
    q2 = db.Column(db.VARCHAR(length=1))
    q3 = db.Column(db.VARCHAR(length=1))
    q4 = db.Column(db.VARCHAR(length=1000))
    q5 = db.Column(db.VARCHAR(length=1000))
    q6 = db.Column(db.VARCHAR(length=1000))
    q7 = db.Column(db.VARCHAR(length=1000))
    q8 = db.Column(db.VARCHAR(length=1))
    q9 = db.Column(db.VARCHAR(length=1000))
    q10 = db.Column(db.VARCHAR(length=1))
    q11 = db.Column(db.VARCHAR(length=1000))
    q12 = db.Column(db.VARCHAR(length=1000))
    q13 = db.Column(db.VARCHAR(length=1000))
    q14 = db.Column(db.VARCHAR(length=1))
    q10yes = db.Column(db.VARCHAR(length=1000))

    def __unicode__(self):
        return self.id
