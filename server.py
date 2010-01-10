import sys
sys.path.append('tornado')
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.template
import hashlib
import random
import re
import os
import traceback

loader = tornado.template.Loader(os.path.join(os.path.join(os.path.realpath(__file__) + '/../'), 'templates'))

class NewPlayerHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")

settings = {'static_path': os.path.join(os.path.realpath(__file__ + '/../'), 'static')}

application = tornado.web.Application(**settings)
application.add_handlers('.*$', [(r'/', NewPlayerHandler)])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9998)
    tornado.ioloop.IOLoop.instance().start()
