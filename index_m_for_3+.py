# -*- coding: utf-8 -*-
from tornado import httpserver,ioloop,options,web
from tornado.options import define,options

__author__ = 'Mu001999'

define('port',default=9500,help='run on the given port',type=int)

class MainHandler(web.RequestHandler):
    def get(self):
        self.write('Test on port:'+str(options.port))

def main():
    print('Test on port:' + str(options.port))
    options.parse_command_line()
    application = web.Application([(r'/',MainHandler),])
    http_server = httpserver.HTTPServer(application)
    http_server.listen(options.port)
    ioloop.IOLoop.current().start()

main()