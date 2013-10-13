#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""
Launch the application. Used by EB.
"""
from xponentialy import load_app

app = load_app()

if __name__ == '__main__':
    app.run()
