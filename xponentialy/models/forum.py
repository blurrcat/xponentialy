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
    date = db.Column(db.DATE)
    message = db.Column(db.VARCHAR(length=2000))


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.INTEGER(display_width=11), primary_key=True,
                   nullable=False)
    description = db.Column(db.VARCHAR(length=200), nullable=False)
    url = db.Column(db.VARCHAR(length=400), nullable=False)
    user_id = db.Column(db.INTEGER(display_width=11), nullable=False)
    post_facebook = db.Column(db.BOOLEAN, nullable=False)
    post_pic = db.Column(db.VARCHAR(length=400), nullable=False)


class PostSubscription(db.Model):
    __tablename__ = 'postsubscription'
    thread_id = db.Column(db.INTEGER(display_width=11),
                          primary_key=True, nullable=False)
    user_id = db.Column(db.INTEGER(display_width=11),
                        primary_key=True, nullable=False)


class ForumThread(db.Model):
    __tablename__ = 'forumthread'
    id = db.Column(db.INTEGER(display_width=11),
                   primary_key=True, nullable=False)
    challenge_id = db.Column(db.SMALLINT(display_width=11), nullable=False)
    create_time = db.Column(db.TIMESTAMP(), nullable=False)
    creator_id = db.Column(db.INTEGER(display_width=11), nullable=False)
    message = db.Column(db.VARCHAR(length=2000), nullable=False)
    archived = db.Column(db.BOOLEAN, nullable=False)
    tutor_only = db.Column(db.BOOLEAN, nullable=False)

    def __str__(self):
        return str(self.id)


class ThreadPost(db.Model):
    __tablename__ = 'threadpost'
    cid = db.Column(db.INTEGER(display_width=11),
                    primary_key=True, nullable=False)
    commenter_id = db.Column(db.INTEGER(display_width=11), nullable=False)
    thread_id = db.Column(db.INTEGER(display_width=11), nullable=False)
    comment = db.Column(db.VARCHAR(length=2000), nullable=False)
    comment_time = db.Column(db.TIMESTAMP(), nullable=False)
    deleted = db.Column(db.INTEGER(display_width=11), nullable=False)