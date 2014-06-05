from eventlet import wsgi
import eventlet

def hello(env, start_response):
   start_response('200 OK', [('Content-Type', 'text/plain')])
   return ['Hello, World!\r\n']

wsgi.server(eventlet.wrap_ssl(eventlet.listen(('localhost', 8457)),certfile='/tmp/HMIUC/ssl/server.crt',keyfile='/tmp/HMIUC/ssl/server.key',server_side=True),hello)

