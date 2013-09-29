#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Harry Liang <blurrcat@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from . import db


class Update(db.Model):
    __tablename__ = 'updates'
    id = db.Column(db.INTEGER(display_width=11), primary_key=True,
                   nullable=False)
    update = db.Column(db.VARCHAR(length=500))
    user_id = db.Column(db.INTEGER(display_width=11))
    type = db.Column(db.VARCHAR(length=10))
    time_updated = db.Column(db.TIMESTAMP(), nullable=False)


class Activity(db.Model):
    __tablename__ = 'activity'
    user_id = db.Column(db.INTEGER(display_width=11),
                        primary_key=True, nullable=False)
    date = db.Column(db.DATE(), primary_key=True, nullable=False)
    steps = db.Column(db.INTEGER(display_width=11))
    floors = db.Column(db.INTEGER(display_width=11))
    calories = db.Column(db.INTEGER(display_width=11))
    active_score = db.Column(db.INTEGER(display_width=11))
    distance = db.Column(db.INTEGER(display_width=11))
    elevation = db.Column(db.INTEGER(display_width=11))
    min_sedentary = db.Column(db.INTEGER(display_width=11))
    min_lightlyactive = db.Column(db.INTEGER(display_width=11))
    min_fairlyactive = db.Column(db.INTEGER(display_width=11))
    min_veryactive = db.Column(db.INTEGER(display_width=11))
    activity_calories = db.Column(db.INTEGER(display_width=11))
    last_update = db.Column(db.TIMESTAMP(), nullable=False)


class IntraDayActivity(db.Model):
    __tablename__ = 'intradayactivity'
    # id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER(display_width=11), nullable=False,
                        primary_key=True)
    activity_time = db.Column(db.DATETIME(), nullable=False, primary_key=True)
    steps = db.Column(db.INTEGER(display_width=11))
    calories = db.Column(db.FLOAT())
    calories_level = db.Column(db.INTEGER(display_width=11))
    floors = db.Column(db.INTEGER(display_width=11))
    elevation = db.Column(db.FLOAT())

    # uc_user_activity = db.UniqueConstraint('user_id', 'activity_time')


class Sleep(db.Model):
    __tablename__ = 'sleep'
    user_id = db.Column(db.INTEGER(display_width=11),
                        primary_key=True, nullable=False)
    date = db.Column(db.DATE(), primary_key=True, nullable=False)
    total_time = db.Column(db.INTEGER(display_width=11))
    time_asleep = db.Column(db.INTEGER(display_width=11))
    start_time = db.Column(db.TIME())
    awaken_count = db.Column(db.INTEGER(display_width=11))
    min_awake = db.Column(db.INTEGER(display_width=11))
    min_to_asleep = db.Column(db.INTEGER(display_width=11))
    min_after_wakeu = db.Column(db.INTEGER(display_width=11))
    efficiency = db.Column(db.INTEGER(display_width=11))