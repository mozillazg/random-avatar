#!/usr/bin/env python
# -*- coding: utf-8 -*-

from avatar.app import app

if __name__ == '__main__':
    app_wsgi = app.wsgifunc()
