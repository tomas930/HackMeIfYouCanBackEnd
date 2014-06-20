# -*- coding: utf-8
#!/usr/bin/python
"""A web.py application powered by gevent"""
from eventlet import wsgi
import eventlet
from gevent.pywsgi import WSGIServer
import sys
import time
import os
import sqlite3
import mail
import json
import crypt
import web
import string
import random
import dbConnector
from dbConnector import *
from mail import *
import sessionControler
from sessionControler import *


# allowed methods in dbConnector 
# getLastID()	return lastID
# addFile(self,login, userFile, extension):
# getUserFile(self,login):	return file
# addNote(self,noteID, login, note):	return True
# getUserNotes(self,login):	return []
# getUserInformation(self,login):		return info
# checkPassword(self, login, password):		return False
# addErrorLog(self, date, message):		return True
# addLog( self,date, message):	return True
# checkIfLoginIsFree(self,login):		return True
# addUserToDB( self,login, password, email, name, surname):		return True


#prefix = 'localhost:8457'

urls = ('/notes', 'Notes',
'/register', 'Register',
'/login', 'Login',
'/reset', 'ResetPassword',
'/upload', 'Upload',
'/', 'Index',
)

web.config.debug = False
app = web.application(urls, locals())

#session = SessionController(app)
connector = dbConnector()

noteIDcounter = connector.getLastID()
passwordReset = ''
badLoginCounter = 0


class Upload:
    def GET(self):
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(myfile={})
        file = open('/home/stud/ficm/database/database.db', 'w')
        file.write(x['myfile'].file.read())
        file.close()
        # TODO insert page address to redirect
        raise web.seeother('')

		
class ResetPassword:
    def GET(self):
        data = web.data()
        data = json.loads(data)
        print (data)
        info = connector.getUserInformation(data['login'])
        passwordReset = ''.join(random.sample(string.ascii_letters, 12))
        sendMail(info[2], 'Password reset', 'Yor password reset key is:' + passwordReset)
        res.status = '200 OK'
        res.cont = 'text/plain'
        res.body = '0'
        return 0
    def POST(self):
        data = web.data()
        data = json.loads(data)
        
        if data['resetKey'] == passwordReset:
            salt = connector.getSalt(login)
            password = crypt.crypt(data['password'], salt)
            for i in range(1, 10):
                password = crypt.crypt(password, salt)		
            connector.updateUserPassword(data['login'], password)
            return json.dumps({'result' : True})
        else:
            return json.dumps({'result' : 'Invalid reset key.'})
        
class Login:
    def POST(self):
        global badLoginCounter
        data = web.data()
        data = json.loads(data)
        login = str(data['login'])
        password = str(data['password'])
        salt = str(connector.getSalt(login))
        password = crypt.crypt(password, salt)
        for i in range(1, 10):
            password = crypt.crypt(password, salt)
        logged = connector.checkPassword( login, password )
        response = {'logged' : logged}
        if logged == True:
            #session.setSession(login)
            web.setcookie('login', login, 3600, secure=True )
        else:
            if badLoginCounter == 5:
                badLoginCounter = 0
                time.sleep(60)
            badLoginCounter = badLoginCounter + 1
        response = json.dumps(response)
        return response

class Register:
    def POST(self):
        data = web.data()
        data = json.loads(data)
        salt = ''.join(random.sample(string.ascii_letters, 2))
        connector.setSalt(data['login'], salt)
        password = crypt.crypt(data['password'], salt)
        for i in range(1, 10):
            password = crypt.crypt(password, salt)
        result = connector.addUserToDB(data['login'], password, data['email'], data['name'], data['surname'])
        if result == True:
            sendMail(data['email'], "Welcome!", "You have been successful registered in our application. Remember, You can reset your password only with this e-mail.")
        return json.dumps({'registered' : result})
	

class Notes:
    def GET(self):
        data = web.data()
        data = json.loads(data)
        result = connector.getUserNotes(data['login'])
        return json.dumps(result)
    def POST(self):
        data = web.data()
        result = connector.addNote(noteIDcounter, data['login'], data['note'])
        response
        if result == True:
            response = {'noteID' : noteIDcounter }
            return json.dumps(response)            
        else:
            return json.dumps({ 'added' : False })

			
def sendMail(sendTo, message, topic):
    sender = mail()
    sender.send(sendTo, message, topic)
    return 0

class Index:
    def GET(self):	   
        return ['Hello, World!\r\n']


wsgi.server(eventlet.wrap_ssl(eventlet.listen(('localhost', 8457)),certfile='/tmp/HMIUC/ssl/server.crt',keyfile='/tmp/HMIUC/ssl/server.key',server_side=True),app.wsgifunc())
