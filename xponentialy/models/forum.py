#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Harry Liang <blurrcat@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from . import db


class EmailMessage(db.Model):
    __tablename__ = 'emailmessage'
    id = db.Column(db.INTEGER(display_width=11), primary_key=True,
                   nullable=False)
    date = db.Column(db.DATETIME())
    message = db.Column(db.VARCHAR(length=2000))

    def __unicode__(self):
        return u'[%s]%s...' % (self.id, self.message[:20])


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.INTEGER(display_width=11), primary_key=True,
                   nullable=False)
    description = db.Column(db.VARCHAR(length=200), nullable=False)
    url = db.Column(db.VARCHAR(length=400), nullable=False)
    user_id = db.Column(db.INTEGER(display_width=11),
                        db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='notifications')
    post_facebook = db.Column(db.BOOLEAN, nullable=False)
    post_pic = db.Column(db.VARCHAR(length=400), nullable=False)

    def __unicode__(self):
        return u'[%s]:%s' % (self.id, self.description)


class ForumThread(db.Model):
    __tablename__ = 'forumthread'
    id = db.Column(db.INTEGER(display_width=11),
                   primary_key=True, nullable=False)
    challenge_id = db.Column(db.SMALLINT(display_width=11), nullable=False)
    create_time = db.Column(db.TIMESTAMP(), nullable=False)
    creator_id = db.Column(db.INTEGER(display_width=11),
                           db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.VARCHAR(length=2000), nullable=False)
    archived = db.Column(db.BOOLEAN, nullable=False)
    tutor_only = db.Column(db.BOOLEAN, nullable=False)
    subscribers = db.relationship(
        'User',
        secondary=db.Table(
            'postsubscription',
            db.Column('thread_id', db.INTEGER(display_width=11),
                      db.ForeignKey('forumthread.id'),
                      primary_key=True, nullable=False),
            db.Column('user_id', db.INTEGER(display_width=11),
                      db.ForeignKey('user.id'),
                      primary_key=True, nullable=False)
        ),
        backref=db.backref('post_subscriptions')
    )
    creator = db.relationship('User', backref='threads')

    def __unicode__(self):
        return u'[%s]%s' % (self.id, self.message[:20])


class ThreadPost(db.Model):
    __tablename__ = 'threadpost'
    id = db.Column(db.INTEGER(display_width=11),
                    primary_key=True, nullable=False)
    commenter_id = db.Column(db.INTEGER(display_width=11),
                             db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', backref='comments')
    thread_id = db.Column(db.INTEGER(display_width=11),
                          db.ForeignKey('forumthread.id'), nullable=False)
    thread = db.relationship('ForumThread', backref='comments')
    comment = db.Column(db.VARCHAR(length=2000), nullable=False)
    comment_time = db.Column(db.DATETIME(), nullable=False)
    deleted = db.Column(db.INTEGER(display_width=11), nullable=False)

    def __unicode__(self):
        return u'[%s]%s' % (self.id, self.comment[:20])
