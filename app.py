# -*- coding: utf-8
#!/usr/bin/python
"""A web.py application powered by gevent"""
from gevent.pywsgi import WSGIServer
import time
import os
import sqlite3
import mail
import json
import crypt
import web
import dbConnector
from dbConnector import *
from mail import *
import sessionControler
from sessionControler import *


# allowed methods in dbConnector 
# getLastID()	return lastID
# addFile(login, userFile)	return True
# getUserFile(self,login):	return file
# addNote(self,noteID, login, note):	return True
# getUserNotes(self,login):	return []
# getUserInformation(self,login):		return info
# checkPassword(self, login, password):		return False
# addErrorLog(self, date, message):		return True
# addLog( self,date, message):	return True
# checkIfLoginIsFree(self,login):		return True
# addUserToDB( self,login, password, email, name, surname):		return True


prefix = '/~okraskat/apps/safetyNote'

urls = (prefix + '/notes/(.*)', 'Notes',
        prefix + '/register/(.*)', 'Register',
        prefix + '/login/(.*)', 'Login',
        prefix + '/(.*)', 'Index',		
        )
		
web.config.debug = False
app = web.application(urls, locals())

session = SessionController(app)
connector = dbConnector()

noteIDcounter = connector.getLastID()

class Login:
    def POST(self):
        data = web.data()
        data = json.loads(data)
        login = data['login']
        password = data['password']
        salt = connector.getSalt(login)
        password = crypt.crypt(password, salt)
        for i in range(1, 10):
            password = crypt.crypt(password, salt)
        logged = connector.checkPassword( login, password )
        response = {'logged' : logged}
        if logged == True:
            session.setSession(login)
            web.setcookie('login', login, 3600, secure=True )
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
            sendMail(data.email, "Welcome!", "You have been successful registered in our application. Remember, You can reset your password only with this e-mail.")
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

			
def sendMail(sendTo, topic, message):
    sender = mail()
    sender.send(sendTo, message, topic)
    return 0



if __name__ == "__main__":
    print ""