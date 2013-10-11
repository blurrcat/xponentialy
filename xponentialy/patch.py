#!/usr/env/bin python
# -*- coding: utf-8 -*-
"""
This script contains patches to third party libraries. They may have bugs
which have not been fixed in their release versions.

Patches include:

1. Flask-Admin==1.0.6: The constructor of :class:`flask_admin.form.TimeField`
doesn't initialize time formats properly. Calls on
:method:`flask_admin.form.TimeField.process_formdata` raises a AttributeError.

The script must be executed before the main flask application is constructed
"""

# Patch 1
import time
import datetime
from flask_admin import form
from wtforms import fields, widgets
from flask.ext.admin.babel import gettext


class TimeField(fields.Field):
    """
        A text field which stores a `datetime.time` object.
        Accepts time string in multiple formats: 20:10, 20:10:00, 10:00 am, 9:30pm, etc.
    """
    widget = widgets.TextInput()

    def __init__(self, label=None, validators=None, formats=None, **kwargs):
        """
            Constructor

            :param label:
                Label
            :param validators:
                Field validators
            :param formats:
                Supported time formats, as a enumerable.
            :param kwargs:
                Any additional parameters
        """
        super(TimeField, self).__init__(label, validators, **kwargs)

        self.formats = formats or ('%H:%M:%S', '%H:%M',
                                  '%I:%M:%S%p', '%I:%M%p',
                                  '%I:%M:%S %p', '%I:%M %p')

    def _value(self):
        if self.raw_data:
            return u' '.join(self.raw_data)
        else:
            return self.data and self.data.strftime(self.formats) or u''

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = u' '.join(valuelist)

            for format in self.formats:
                try:
                    timetuple = time.strptime(date_str, format)
                    self.data = datetime.time(timetuple.tm_hour,
                                              timetuple.tm_min,
                                              timetuple.tm_sec)
                    return
                except ValueError:
                    pass

            raise ValueError(gettext('Invalid time format'))

form.TimeField = TimeField