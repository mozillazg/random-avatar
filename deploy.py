#!/usr/bin/env python
# -*- coding: utf-8 -*-

from avatar.app import app

app_wsgi = app.wsgifunc()
