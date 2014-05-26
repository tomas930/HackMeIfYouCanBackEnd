# -*- coding: utf-8
#!/usr/bin/python
"""A web.py application powered by gevent"""
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
import time
import web
import os

urls = ('/', "index",
        '/long', 'long_polling',
        '/check', 'check')


class index:
    def GET(self):
        return '<html>Hello, world!<br><a href="/long">/long</a></html>'


class long_polling:
    # Since gevent's WSGIServer executes each incoming connection in a separate greenlet
    # long running requests such as this one don't block one another;
    # and thanks to "monkey.patch_all()" statement at the top, thread-local storage used by web.ctx
    # becomes greenlet-local storage thus making requests isolated as they should be.
    def GET(self):
        print 'GET /long'
        time.sleep(10)  # possible to block the request indefinitely, without harming others
        return 'Hello, 10 seconds later'

class check:
    # Since gevent's WSGIServer executes each incoming connection in a separate greenlet
    # long running requests such as this one don't block one another;
    # and thanks to "monkey.patch_all()" statement at the top, thread-local storage used by web.ctx
    # becomes greenlet-local storage thus making requests isolated as they should be.
    def GET(self):
        print 'GET /check'
        while not os.path.exists('/home/ee/stud/ficm/www/plik'):
             time.sleep(0.5)
        return 'Plik sie pojawil\n'

        
        

if __name__ == "__main__":
    app = web.application(urls, globals())
    wsgi = app.wsgifunc()
    print "Działam na porcie 8081"
    WSGIServer(('', 8081), wsgi).serve_forever()
