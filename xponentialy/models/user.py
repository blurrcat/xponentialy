#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Harry Liang <blurrcat@gmail.com>
"""

"""
from . import db
from flask.ext.security import UserMixin, RoleMixin


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __unicode__(self):
        return u'%s:%s' % (self.name, self.description[:20] + '..')


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.INTEGER(display_width=11),
                   primary_key=True, nullable=False)
    first_name = db.Column(db.VARCHAR(length=20))
    last_name = db.Column(db.VARCHAR(length=20))
    fitbit_id = db.Column(db.VARCHAR(length=10))
    oauth_token = db.Column(db.VARCHAR(length=40))
    oauth_secret = db.Column(db.VARCHAR(length=40))
    profile_pic = db.Column(db.VARCHAR(length=200))
    gender = db.Column(db.VARCHAR(length=10))
    house_id = db.Column(db.INTEGER(display_width=11),
                         db.ForeignKey('house.id'))
    company_id = db.Column(db.INTEGER, db.ForeignKey('company.id'))
    username = db.Column(db.VARCHAR(length=20))
    email = db.Column(db.VARCHAR(length=40), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime())
    admin = db.Column(db.BOOLEAN)
    phantom = db.Column(db.BOOLEAN)
    staff = db.Column(db.BOOLEAN)
    leader = db.Column(db.BOOLEAN)
    points = db.Column(db.INTEGER(display_width=11))
    fb = db.Column(db.BOOLEAN, default=False)
    badge_email_unsub = db.Column(db.BOOLEAN, default=True)
    daily_email_unsub = db.Column(db.BOOLEAN, default=True)
    challenge_email_unsub = db.Column(db.BOOLEAN, default=True)
    hide_progress = db.Column(db.BOOLEAN, default=False)

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.DateTime())
    current_login_ip = db.Column(db.String(50))
    login_count = db.Column(db.String(50))

    roles = db.relationship(
        'Role',
        secondary=db.Table(
            'roles_users',
            db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
            db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
        ),
        backref=db.backref('users', lazy='dynamic')
    )

    def __unicode__(self):
        return u'[%s]%s' % (self.id, self.username)


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(length=128), nullable=False)
    description = db.Column(db.String(length=255))
    profile_pic = db.Column(db.VARCHAR(length=200))
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
