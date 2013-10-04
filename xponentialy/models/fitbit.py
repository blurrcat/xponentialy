#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Harry Liang <blurrcat@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
import time
from datetime import datetime
from . import db


class Update(db.Model):
    __tablename__ = 'updates'
    id = db.Column(db.INTEGER(display_width=11), primary_key=True,
                   nullable=False)
    update = db.Column(db.VARCHAR(length=500))
    user_id = db.Column(db.INTEGER(display_width=11),
                        db.ForeignKey('user.id'),
                        nullable=False)
    type = db.Column(db.VARCHAR(length=10))
    time_updated = db.Column(db.TIMESTAMP(), nullable=False)
    user = db.relationship('User', backref='updates')

    def __unicode__(self):
        return u'[%s]%s' % (self.id, self.update[:20])


class Activity(db.Model):
    __tablename__ = 'activity'
    user_id = db.Column(db.INTEGER(display_width=11),
                        db.ForeignKey('user.id'),
                        primary_key=True, nullable=False)
    user = db.relationship('User', backref='activities')
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

    def __unicode__(self):
        return u'[%s]steps: %s; floors: %s; distance: %s; elevation: %s' % (
            self.id, self.steps, self.floors, self.distance, self.elevation
        )

    def update(self, data):
        summary = data['summary']
        self.steps = summary.get('steps', 0)
        self.floors = summary.get('floors', 0)
        # todo: confirm calories field name
        self.calories = summary.get('caloriesOut', 0)
        self.active_score = summary.get('activeScore', 0)
        # todo: confirm distance field
        for item in summary['distances']:
            if item['activity'] == 'total':
                self.distance = item['distance']
                break
        self.elevation = summary.get('elevation')
        self.min_sedentary = summary['sedentaryMinutes']
        self.min_lightlyactive = summary['lightlyActiveMinutes']
        self.min_fairlyactive = summary['fairlyActiveMinutes']
        self.min_veryactive = summary['veryActiveMinutes']
        self.activity_calories = summary.get('activityCalories', 0)
        self.last_update = time.time()


class IntraDayActivity(db.Model):
    __tablename__ = 'intradayactivity'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER(display_width=11),
                        db.ForeignKey('user.id'),
                        nullable=False)
    user = db.relationship('User', backref='intraday_activities')
    activity_time = db.Column(db.DATETIME(), nullable=False)
    steps = db.Column(db.INTEGER(display_width=11))
    calories = db.Column(db.FLOAT())
    calories_level = db.Column(db.INTEGER(display_width=11))
    floors = db.Column(db.INTEGER(display_width=11))
    elevation = db.Column(db.FLOAT())

    __table_args__ = (
        db.UniqueConstraint('user_id', 'activity_time',
                            name='uc_user_activity'),
    )

    def __unicode__(self):
        return u'[%s]steps: %s; calories: %s; floors: %s; elevation: %s' % (
            self.id, self.steps, self.calories, self.floors, self.elevation
        )


class Sleep(db.Model):
    __tablename__ = 'sleep'
    user_id = db.Column(db.INTEGER(display_width=11),
                        db.ForeignKey('user.id'),
                        primary_key=True, nullable=False)
    user = db.relationship('User', backref='sleeps')
    date = db.Column(db.DATE(), primary_key=True, nullable=False)
    total_time = db.Column(db.INTEGER(display_width=11))
    time_asleep = db.Column(db.INTEGER(display_width=11))
    start_time = db.Column(db.DATETIME())
    awaken_count = db.Column(db.INTEGER(display_width=11))
    min_awake = db.Column(db.INTEGER(display_width=11))
    min_to_asleep = db.Column(db.INTEGER(display_width=11))
    min_after_wake = db.Column(db.INTEGER(display_width=11))
    efficiency = db.Column(db.INTEGER(display_width=11))

    def __unicode__(self):
        return u'[%s]total_time: %s; date: %s; start_time: %s; efficiency: %s' % (
            self.id, self.total_time, self.date, self.start_time, self.efficiency
        )

    def update(self, data):
        summary = data['summary']
        self.total_time = summary['totalTimeInBed']
        self.time_asleep = summary['totalMinutesAsleep']
        # todo: what if we have multiple sleep records?
        if summary['totalSleepRecords'] >= 1:
            sleep = data['sleep'][0]
            self.start_time = datetime.strptime(
                sleep['startTime'], '%Y-%m-%dT%H:%M:%S.%f')
            self.awaken_count = sleep['awakeningsCount']
            self.min_awake = sleep['minutesAwake']
            self.min_to_asleep = sleep['minutesToFallAsleep']
            self.min_after_wake = sleep['minutesAfterWakeup']
            self.efficiency = sleep['efficiency']


__models = {
    'activity': Activity,
    'sleep': Sleep
}


def get_model_by_name(name):
    return __models.get(name)