#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""

"""
from flask import request, flash, redirect, render_template, url_for
from flask.ext.peewee.admin import Admin, ModelAdmin, AdminPanel
from flask.ext.peewee.utils import make_password
from wtforms import PasswordField, Form
from wtforms.validators import Length, Email, EqualTo, DataRequired
from wtforms.validators import ValidationError
from wtfpeewee.orm import model_fields

from xponentialy import app
from xponentialy import models
from xponentialy.auth import auth


admin = Admin(app, auth, branding='Xponentialy Admin')


class UserAdmin(ModelAdmin):
    exclude = ['password']

admin.register(models.User, UserAdmin)
registered = ['User']
for name in models.__all__:
    if name not in registered:
        admin.register(getattr(models, name))


class Unique(object):

    def __init__(self, model, attribute, message=None):
        self.model = model
        self.attribute = attribute
        self.message = message or '%s has already been taken'

    def __call__(self, form, field):
        _attr = getattr(self.model, self.attribute)
        if self.model.select(_attr).where(_attr == field.data).exists():
            raise ValidationError(message=self.message % field.data)


def get_user_create_form():
    field_dict = model_fields(
        models.User,
        only=['username', 'email', 'company', 'house'],
        field_args={
            'username': dict(
                validators=[DataRequired(), Length(min=4, max=25),
                            Unique(models.User, 'username')],
                label=u'',
            ),
            'email': dict(validators=[DataRequired(), Email(),
                                      Unique(models.User, 'email')]),
        }
    )
    field_dict.update({
        'password': PasswordField(
            'Password', [
                DataRequired(),
                Length(min=6, max=15),
                EqualTo('confirm', message='Password must match')
            ]
        ),
        'confirm': PasswordField(
            'Password Again'
        )
    })
    field_dict['house'].kwargs['allow_blank'] = False
    field_dict['company'].kwargs['allow_blank'] = False
    return type('UserCreateForm', (Form, ), field_dict)

UserCreateForm = get_user_create_form()


class UserCreatePanel(AdminPanel):
    template_name = 'admin/create_user_panel.html'


@admin.blueprint.route('/create_user/form', methods=['GET', 'POST'])
def admin_create_user():
    form = UserCreateForm(request.form)
    if request.method == 'POST' and form.validate():
        models.User.create(
            username=form.username.data,
            email=form.email.data,
            company=form.company.data,
            house=form.house.data,
            password=make_password(form.password.data)
        )
        flash('User %s has been created' % form.username.data)
        return redirect(url_for('.index'))
    return render_template('admin/create_user.html', form=form)

admin.register_panel('Create User', UserCreatePanel)
admin.setup()