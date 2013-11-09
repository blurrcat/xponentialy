#!/usr/env/bin python
# -*- coding: utf-8 -*-
import datetime

from flask import current_app
from flask.ext.peewee.auth import BaseUser
from peewee import *
from fitbit import Fitbit

from xponentialy import db
from xponentialy.utils import time_range

__all__ = ['Company', 'House', 'User', 'Survey', 'Activity',
           'IntradayActivity', 'Sleep', 'Update', 'Badge', 'UserBadge',
           'ForumThread', 'Challenge', 'ChallengeParticipant', 'InvalidPeriod',
           'Notification', 'Postsubscription', 'Emailmessage', 'Threadpost']


class Company(db.Model):
    description = CharField(null=True)
    name = CharField(unique=True)
    profile_pic = CharField(null=True)

    class Meta:
        db_table = 'company'

    def __unicode__(self):
        return self.name


class House(db.Model):
    name = CharField()
    picture = CharField(null=True)
    company = ForeignKeyField(rel_model=Company, related_name='houses',
                              db_column='company_id')

    class Meta:
        db_table = 'house'

    @classmethod
    def get_leaders(cls, cid, days):
        start, end = time_range(days)
        points = fn.Sum(Challenge.points)
        return House.select(
            House, points.alias('points')) \
            .join(ChallengeParticipant) \
            .join(Challenge).group_by(User.id) \
            .where(ChallengeParticipant.complete_time.between(start, end)) \
            .where(House.company == cid) \
            .order_by(points.desc())

    def __unicode__(self):
        return self.name


class User(db.Model, BaseUser):
    active = IntegerField(null=True)
    admin = IntegerField(null=True)
    badge_email_unsub = IntegerField(null=True)
    challenge_email_unsub = IntegerField(null=True)
    company = ForeignKeyField(null=True, db_column='company_id',
                              rel_model=Company, related_name='users')
    confirmed_at = DateTimeField(null=True)
    current_login_at = DateTimeField(null=True)
    current_login_ip = CharField(null=True)
    daily_email_unsub = IntegerField(null=True)
    email = CharField(unique=True)
    fb = IntegerField(null=True)
    first_name = CharField(null=True)
    fitbit = CharField(null=True, db_column='fitbit_id')
    gender = CharField(null=True)
    hide_progress = IntegerField(null=True)
    house = ForeignKeyField(null=True, db_column='house_id', rel_model=House,
                            related_name='users')
    last_login_at = DateTimeField(null=True)
    last_login_ip = DateTimeField(null=True)
    last_name = CharField(null=True)
    leader = IntegerField(null=True)
    login_count = IntegerField(null=True)
    oauth_secret = CharField(null=True)
    oauth_token = CharField(null=True)
    password = CharField()
    phantom = IntegerField(null=True)
    points = IntegerField(null=True)
    avatar = CharField(null=True)
    staff = IntegerField(null=True)
    username = CharField(null=True, unique=True)

    challenge_num = property(lambda self: self.challenges.count())
    rank = property(lambda self: 1)  # Todo: implement rank

    class Meta:
        db_table = 'user'

    @classmethod
    def get_leaders(cls, cid, days):
        start, end = time_range(days)
        challenge_completed = fn.Count(ChallengeParticipant.id)
        return User.select(
            User, challenge_completed.alias('challenge_completed')) \
            .join(ChallengeParticipant).group_by(User.id) \
            .where(ChallengeParticipant.complete_time.between(start, end)) \
            .where(User.company == cid).where(User.active) \
            .order_by(challenge_completed.desc())

    def get_fitbit_client(self):
        return Fitbit(
            current_app.config['FITBIT_KEY'],
            current_app.config['FITBIT_SECRET'],
            user_key=self.oauth_token,
            user_secret=self.oauth_secret
        )

    def __unicode__(self):
        return self.username


class Survey(db.Model):
    q0 = CharField(null=True)
    q1 = CharField(null=True)
    q10 = CharField(null=True)
    q10yes = CharField(null=True)
    q11 = CharField(null=True)
    q12 = CharField(null=True)
    q13 = CharField(null=True)
    q14 = CharField(null=True)
    q2 = CharField(null=True)
    q3 = CharField(null=True)
    q4 = CharField(null=True)
    q5 = CharField(null=True)
    q6 = CharField(null=True)
    q7 = CharField(null=True)
    q8 = CharField(null=True)
    q9 = CharField(null=True)
    user = ForeignKeyField(db_column='user_id', rel_model=User,
                           related_name='survey')

    class Meta:
        db_table = 'survey'

    def __unicode__(self):
        return u'survey[%d]' % self.id


class Activity(db.Model):
    active_score = IntegerField(null=True)
    activity_calories = IntegerField(null=True)
    calories = IntegerField(null=True)
    date = DateField()
    distance = IntegerField(null=True)
    elevation = IntegerField(null=True)
    floors = IntegerField(null=True)
    last_update = DateTimeField(null=True)
    min_fairlyactive = IntegerField(null=True)
    min_lightlyactive = IntegerField(null=True)
    min_sedentary = IntegerField(null=True)
    min_veryactive = IntegerField(null=True)
    steps = IntegerField(null=True)
    user = ForeignKeyField(db_column='user_id', rel_model=User,
                           related_name='activities')

    class Meta:
        db_table = 'activity'
        indexes = (
            (('user', 'date'), True),
        )
        order_by = ('-date', )

    def update_from_fitbit(self, data):
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
        self.elevation = summary.get('elevation', None)
        self.min_sedentary = summary.get('sedentaryMinutes', None)
        self.min_lightlyactive = summary.get('lightlyActiveMinutes', None)
        self.min_fairlyactive = summary.get('fairlyActiveMinutes', None)
        self.min_veryactive = summary.get('veryActiveMinutes', None)
        self.activity_calories = summary.get('activityCalories', None)
        self.last_update = datetime.datetime.utcnow()

    def __unicode__(self):
        return u'Activity of %s on %s' % (self.user, self.date)


class IntradayActivity(db.Model):
    activity_time = DateTimeField()
    calories = FloatField(null=True)
    calories_level = IntegerField(null=True)
    elevation = FloatField(null=True)
    floors = IntegerField(null=True)
    steps = IntegerField(null=True)
    user = ForeignKeyField(db_column='user_id', rel_model=User,
                           related_name='intraday_activites')

    class Meta:
        db_table = 'intradayactivity'
        order_by = ('-activity_time',)
        indexes = (
            (('user', 'activity_time'), True),
        )

    def update_from_fitbit(self, data, resource):
        if resource == 'calories':
            self.calories = data['value']
            self.calories_level = data['level']
        else:
            setattr(self, resource, data['value'])


    def __unicode__(self):
        return 'IntradayActivity of %s at %s' % (self.user, self.activity_time)


class Sleep(db.Model):
    awaken_count = IntegerField(null=True)
    date = DateField()
    efficiency = IntegerField(null=True)
    min_after_wake = IntegerField(null=True)
    min_awake = IntegerField(null=True)
    min_to_asleep = IntegerField(null=True)
    start_time = DateTimeField(null=True)
    time_asleep = IntegerField(null=True)
    total_time = IntegerField(null=True)
    user = ForeignKeyField(db_column='user_id', rel_model=User,
                           related_name='sleeps')

    class Meta:
        db_table = 'sleep'
        order_by = ('-date',)

    def update_from_fitbit(self, data):
        summary = data['summary']
        self.total_time = summary['totalTimeInBed']
        self.time_asleep = summary['totalMinutesAsleep']
        for sleep in data['sleep']:
            self.start_time = datetime.datetime.strptime(
                sleep['startTime'], '%Y-%m-%dT%H:%M:%S.%f')
            self.awaken_count = sleep.get('awakeningsCount', None)
            self.min_awake = sleep.get('minutesAwake', None)
            self.min_to_asleep = sleep.get('minutesToFallAsleep', None)
            self.min_after_wake = sleep.get('minutesAfterWakeup', None)
            self.efficiency = sleep.get('efficiency', None)

    def __unicode__(self):
        return u'Sleep of %s on %s' % (self.user, self.date)


class Update(db.Model):
    time_updated = DateTimeField(null=True)
    type = CharField()
    update = CharField()
    user = ForeignKeyField(db_column='user_id', rel_model=User,
                           related_name='updates')

    class Meta:
        db_table = 'updates'
        order_by = ('-time_updated',)
        indexes = (
            (('user', ), False),
            (('time_updated',), False),
        )

    @classmethod
    def last_update_time(cls, user, collection):
        try:
            update = Update.get(Update.user == user, Update.type == collection)
            return update.time_updated
        except Update.DoesNotExist:
            return None

    def __unicode__(self):
        return u'type: %s; user: %s; time: %s' % (
            self.type, self.user, self.time_updated)


__models = {
    'activities': Activity,
    'sleep': Sleep
}


def get_model_by_name(name):
    return __models.get(name)


# competition
class Badge(db.Model):
    avatar = CharField()
    description = CharField(null=True)
    min_points = IntegerField()
    name = CharField()

    class Meta:
        db_table = 'badge'

    def __unicode__(self):
        return self.name


class UserBadge(db.Model):
    badge = ForeignKeyField(db_column='badge_id', rel_model=Badge)
    date = DateField()
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta:
        db_table = 'userbadge'

    def __unicode__(self):
        return '%s earned %s on %s' % (self.user, self.badge, self.date)


class ForumThread(db.Model):
    archived = IntegerField()
    create_time = DateTimeField(default=datetime.datetime.utcnow)
    creator = ForeignKeyField(db_column='creator_id', rel_model=User,
                              related_name='threads')
    message = CharField()
    tutor_only = IntegerField()

    class Meta:
        db_table = 'forumthread'

    def __unicode__(self):
        return self.message[:20]


class Challenge(db.Model):
    badge_pic = CharField(null=True)
    category = IntegerField()
    description = CharField()
    end_time = DateTimeField(null=True)
    floor_value = IntegerField(null=True)
    points = IntegerField()
    quota = IntegerField()
    sleep_time = TimeField(null=True)
    sleep_value = IntegerField(null=True)
    start_time = DateTimeField(default=datetime.datetime.utcnow)
    steps_value = IntegerField(null=True)
    thread = ForeignKeyField(null=True, db_column='thread_id',
                             rel_model=ForumThread, related_name='challenge')
    title = CharField()

    class Meta:
        db_table = 'challenge'

    def __unicode__(self):
        return self.description


class ChallengeParticipant(db.Model):
    category = IntegerField(null=True)
    challenge = ForeignKeyField(db_column='challenge_id', rel_model=Challenge,
                                related_name='participants')
    complete_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)
    id = BigIntegerField()
    inactive = IntegerField(null=True)
    progress = FloatField(null=True, default=0)
    start_time = DateTimeField(null=True, default=datetime.datetime.utcnow)
    user = ForeignKeyField(db_column='user_id', rel_model=User,
                           related_name='challenges')
    house = ForeignKeyField(db_column='house_id', rel_model=House,
                            relate_name='challenges')

    class Meta:
        db_table = 'challengeparticipant'

        indexes = (
            (('user', 'challenge'), True),
        )

    def __unicode__(self):
        return u'%s in challenge %s' % (self.user, self.challenge)


class InvalidPeriod(db.Model):
    end_date = DateField()
    start_date = DateField()
    user = ForeignKeyField(db_column='user_id', rel_model=User,
                           related_name='invalid_periods')

    class Meta:
        db_table = 'invalidperiod'

    def __unicode__(self):
        return u'%s: %s - %s' % (self.user, self.start_date, self.end_date)


class Notification(db.Model):
    description = CharField(null=True)
    post_facebook = IntegerField()
    post_pic = CharField(null=True)
    url = CharField(null=True)
    user = ForeignKeyField(db_column='user_id', rel_model=User,
                           related_name='notifications')

    class Meta:
        db_table = 'notification'

    def __unicode__(self):
        return self.description


class Postsubscription(db.Model):
    thread = ForeignKeyField(db_column='thread_id', rel_model=ForumThread)
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta:
        db_table = 'postsubscription'


class Emailmessage(db.Model):
    date = DateTimeField(default=datetime.datetime.utcnow)
    message = CharField()

    class Meta:
        db_table = 'emailmessage'

    def __unicode__(self):
        return self.message


class Threadpost(db.Model):
    comment = CharField()
    comment_time = DateTimeField(default=datetime.datetime.utcnow)
    commenter = ForeignKeyField(db_column='commenter_id', rel_model=User,
                                related_name='comments')
    deleted = BooleanField(default=False)
    thread = ForeignKeyField(db_column='thread_id', rel_model=ForumThread,
                             related_name='comments')

    class Meta:
        db_table = 'threadpost'

    def __unicode__(self):
        return self.comment[:20]