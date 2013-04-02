#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from cStringIO import StringIO

import web
from utils.visicon import Visicon

urls = (
    '/([1-9]\d+)?', 'Index',
    '/.*', 'Index',
    '/(.*)/', 'Redirect',
)

app = web.application(urls, globals())


class Redirect(object):
    def GET(self, path):
        return web.seeother('/' + path)


class Index(object):
    def GET(self, size=30):
        ip = web.ctx.ip
        try:
            size = int(size)
        except TypeError:
            size = 30
        size = size if size <= 100 else 30  # limit avatar size

        img = Visicon(ip, str(time()), size).draw_image()
        temp_img = StringIO()
        img.save(temp_img, 'png')
        img_data = temp_img.getvalue()
        temp_img.close()

        web.header('Cache-Control', 'no-cache')
        web.header('Content-Type', 'image/png')
        return img_data

if __name__ == '__main__':
    web.config.debug = True
    app.run()
