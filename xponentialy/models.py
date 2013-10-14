#!/usr/env/bin python
# -*- coding: utf-8 -*-
import datetime

from flask.ext.peewee.auth import BaseUser
from peewee import *

from xponentialy import db

__all__ = ['House', 'User', 'Company', 'Survey', 'Activity',
           'IntradayActivity', 'Sleep', 'Update', 'Badge', 'UserBadge',
           'ForumThread', 'Challenge', 'ChallengeParticipant', 'InvalidPeriod',
           'Notification', 'Postsubscription', 'Emailmessage', 'Threadpost']


class House(db.Model):
    name = CharField()
    picture = CharField(null=True)

    class Meta:
        db_table = 'house'

    def __unicode__(self):
        return self.name


class User(db.Model, BaseUser):
    active = IntegerField(null=True)
    admin = IntegerField(null=True)
    badge_email_unsub = IntegerField(null=True)
    challenge_email_unsub = IntegerField(null=True)
    company = IntegerField(null=True, db_column='company_id')
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
    house = ForeignKeyField(null=True, db_column='house_id', rel_model=House)
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
    profile_pic = CharField(null=True)
    staff = IntegerField(null=True)
    username = CharField(null=True, unique=True)

    class Meta:
        db_table = 'user'

    def __unicode__(self):
        return self.username


class Company(db.Model):
    description = CharField(null=True)
    name = CharField(unique=True)
    profile_pic = CharField(null=True)

    class Meta:
        db_table = 'company'

    def __unicode__(self):
        return self.name


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
    user = ForeignKeyField(db_column='user_id', rel_model=User)

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
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta:
        db_table = 'activity'

    def __unicode__(self):
        return u'Activity of %s on %s' % (self.user_id, self.date)


class IntradayActivity(db.Model):
    activity_time = DateTimeField()
    calories = FloatField(null=True)
    calories_level = IntegerField(null=True)
    elevation = FloatField(null=True)
    floors = IntegerField(null=True)
    steps = IntegerField(null=True)
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta:
        db_table = 'intradayactivity'

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
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta:
        db_table = 'sleep'

    def __unicode__(self):
        return u'Sleep of %s on %s' % (self.user, self.date)


class Update(db.Model):
    time_updated = DateTimeField(null=True)
    type = CharField()
    update = CharField()
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta:
        db_table = 'updates'

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
    badge_pic = CharField()
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
    challenge = IntegerField(db_column='challenge_id')
    create_time = DateTimeField(default=datetime.datetime.utcnow)
    creator = ForeignKeyField(db_column='creator_id', rel_model=User)
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
                             rel_model=ForumThread)
    title = CharField()

    class Meta:
        db_table = 'challenge'

    def __unicode__(self):
        return self.description


class ChallengeParticipant(db.Model):
    category = IntegerField(null=True)
    challenge = ForeignKeyField(db_column='challenge_id', rel_model=Challenge)
    complete_time = DateTimeField(null=True)
    end_time = DateTimeField()
    id = BigIntegerField()
    inactive = IntegerField(null=True)
    progress = FloatField(null=True, default=0)
    start_time = DateTimeField(null=True, default=datetime.datetime.utcnow)
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta:
        db_table = 'challengeparticipant'

    def __unicode__(self):
        return u'%s in challenge %s' % (self.user, self.challenge)


class InvalidPeriod(db.Model):
    end_date = DateField()
    start_date = DateField()
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta:
        db_table = 'invalidperiod'

    def __unicode__(self):
        return u'%s: %s - %s' % (self.user, self.start_date, self.end_date)


class Notification(db.Model):
    description = CharField(null=True)
    post_facebook = IntegerField()
    post_pic = CharField(null=True)
    url = CharField(null=True)
    user = ForeignKeyField(db_column='user_id', rel_model=User)

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
    commenter = ForeignKeyField(db_column='commenter_id', rel_model=User)
    deleted = BooleanField(default=False)
    thread = ForeignKeyField(db_column='thread_id', rel_model=ForumThread)

    class Meta:
        db_table = 'threadpost'

    def __unicode__(self):
        return self.comment[:20]