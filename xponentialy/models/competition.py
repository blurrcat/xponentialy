#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Harry Liang <blurrcat@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from . import db


class House(db.Model):
    __tablename__ = 'house'
    id = db.Column(db.INTEGER(display_width=11),
                   primary_key=True, nullable=False)
    name = db.Column(db.VARCHAR(length=20), nullable=False)
    picture = db.Column(db.VARCHAR(length=100))


class Badge(db.Model):
    __tablename__ = 'badge'
    id = db.Column(db.INTEGER(display_width=11),
                   primary_key=True, nullable=False)
    name = db.Column(db.VARCHAR(length=128), nullable=False)
    badge_pic = db.Column(db.VARCHAR(length=128), nullable=False)
    min_points = db.Column(db.INTEGER(display_width=11), nullable=False)
    description = db.Column(db.VARCHAR(length=256))
    users = db.relationship('UserBadge', backref='badges')

    def __str__(self):
        return self.name


class UserBadge(db.Model):
    __tablename__ = 'userbadge'
    user_id = db.Column(db.INTEGER(display_width=11), db.ForeignKey('user.id'),
                        primary_key=True, nullable=False)
    badge_id = db.Column(db.INTEGER(display_width=11),
                         db.ForeignKey('badge.id'), primary_key=True,
                         nullable=False)
    date = db.Column(db.DATE, nullable=False)
    user = db.relationship('User')


class Challenge(db.Model):
    __tablename__ = 'challenge'
    id = db.Column(db.INTEGER(display_width=11),
                   primary_key=True, nullable=False)
    title = db.Column(db.VARCHAR(length=100), nullable=False)
    description = db.Column(db.VARCHAR(length=500), nullable=False)
    points = db.Column(db.INTEGER(display_width=11), nullable=False)
    badge_pic = db.Column(db.VARCHAR(length=400), nullable=False)
    thread_id = db.Column(db.INTEGER(display_width=11),
                          db.ForeignKey('forumthread.id'))
    thread = db.relationship('ForumThread',
                             backref=db.backref('challenge', uselist=False))
    category = db.Column(db.INTEGER(display_width=11), nullable=False)
    start_time = db.Column(db.DATETIME, nullable=False)
    end_time = db.Column(db.DATETIME, nullable=False)
    steps_value = db.Column(db.INTEGER(display_width=11), nullable=False)
    floor_value = db.Column(db.INTEGER(display_width=11), nullable=False)
    sleep_value = db.Column(db.INTEGER(display_width=11), nullable=False)
    sleep_time = db.Column(db.TIME, nullable=False)
    quota = db.Column(db.INTEGER(display_width=11))
    participants = db.relationship('ChallengeParticipant',
                                   backref='challenges')

    def __str__(self):
        return self.title


class ChallengeParticipant(db.Model):
    __tablename__ = 'challengeparticipant'
    id = db.Column(db.BIGINT(display_width=20),
                   primary_key=True, nullable=False)
    user_id = db.Column(db.INTEGER(display_width=11), db.ForeignKey('user.id'),
                        nullable=False)
    challenge_id = db.Column(db.INTEGER(display_width=11),
                             db.ForeignKey('challenge.id'),
                             nullable=False)
    user = db.relationship('User')
    start_time = db.Column(db.TIMESTAMP(), nullable=False)
    complete_time = db.Column(db.TIMESTAMP(), nullable=False)
    end_time = db.Column(db.TIMESTAMP(), nullable=False)
    progress = db.Column(db.FLOAT)
    category = db.Column(db.INTEGER(display_width=11))
    inactive = db.Column(db.INTEGER(display_width=1), nullable=False)


class InvalidPeriod(db.Model):
    __tablename__ = 'invalidperiod'
    id = db.Column(db.INTEGER(display_width=11),
                   primary_key=True, nullable=False)
    user_id = db.Column(db.INTEGER(display_width=11))
    start_date = db.Column(db.DATE())
    end_date = db.Column(db.DATE())