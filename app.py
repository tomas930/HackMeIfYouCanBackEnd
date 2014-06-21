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
import hashlib
import web
import string
import random
import dbConnector
from dbConnector import *
from mail import *
import sessionControler
from sessionControler import *
import urllib2
import cookielib

urls = ('/notes/(.*)', 'Notes',
'/register', 'Register',
'/login', 'Login',
'/logout', 'Logout',
'/reset', 'ResetPassword',
'/resetKey/(.*)', 'Reseter',
'/upload', 'Upload',
'/', 'Index',
)

web.config.debug = False
app = web.application(urls, locals())

connector = dbConnector()

noteIDcounter = connector.getLastID()
badLoginCounter = 0


class Upload:
    def GET(self):
        try:
            if connector.logged(web.cookies().get('sessionId')) == False:
                return web.notfound()
            connector.updateSession(web.cookies().get('sessionId'))   
            web.setcookie('sessionId', web.cookies().get('sessionId'), 3600, secure=True )
            return """<html><head></head><body><form method="POST" enctype="multipart/form-data" action=""><input type="file" name="myfile" /><br/><input type="submit" /></form></body></html>"""
        except AttributeError:
            return None
        

    def POST(self):
        try:
            if connector.logged(web.cookies().get('sessionId')) == False:
                return web.notfound()
            connector.updateSession(web.cookies().get('sessionId'))
            web.setcookie('sessionId', web.cookies().get('sessionId'), 3600, secure=True )
            x = web.input(myfile={})
            file = open('/home/stud/ficm/database/database.db', 'w')
            file.write(x['myfile'].file.read())
            file.close()
            # TODO insert page address to redirect
            raise web.seeother('')
        except AttributeError:
            return None

class Logout:
    def POST(self):
        try:
            conncector.killSession(web.cookies().get('sessionId'))
            return json.dumps({'result' : "true"})
        except AttributeError:
            return json.dumps({'result' : 'false'})		
class Reseter:
    def GET(self,arg):
        login = connector.getLoginByResetKey(arg)
        connector.enableResetPassword(login)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        return opener.open('https://len.iem.pw.edu.pl:4443/redirect.html')
class ResetPassword:
    def GET(self, arg):
        login = arg
        info = connector.getUserInformation(login)
        passwordReset = ''.join(random.sample(string.ascii_letters, 24))
        m = hashlib.sha256()
        m.update(passwordReset)
        passwordReset = m.hexdigest()
        passwordReset = "https://volt.iem.pw.edu.pl:7777/resetKey/" + passwordReset
        connector.addResetKey(login, passwordReset)
        sendMail(info[2], 'Password reset', 'To reset your password please click this link:\n' + passwordReset)
        res.status = '200 OK'
        res.cont = 'text/plain'
        res.body = '0'
        return 0
    def POST(self):
        data = web.data()
        data = json.loads(data)
        
        if connector.canResetPassword(data['login']) == True:
            salt = connector.getSalt(data['login'])
            connector.disableResetPassword(data['login'])
            m = hashlib.sha256()
            m.update(salt)
            m.update(data['password'])
            password = m.hexdigest()
            for i in range(1, 2):
                m = hashlib.sha256()
                m.update(salt)
                m.update(data['password'])
                password = m.hexdigest()	
            connector.updateUserPassword(data['login'], password)
            return json.dumps({'result' : True})
        else:
            return json.dumps({'result' : 'User can not reset password.'})
        
class Login:
    def POST(self):
        global badLoginCounter
        data = web.data()
        data = json.loads(data)
        login = str(data['login'])
        password = str(data['password'])
        salt = str(connector.getSalt(login))
        m = hashlib.sha256()
        m.update(salt)
        m.update(data['password'])
        password = m.hexdigest()
        for i in range(1, 2):
            m = hashlib.sha256()
            m.update(salt)
            m.update(data['password'])
            password = m.hexdigest()
        logged = connector.checkPassword( login, password )
        response = {'logged' : logged}
        if logged == True:
            sessionId = connector.setSession(login)
            web.setcookie('sessionId', sessionId, 3600, secure=True )
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
        if connector.emailFree(data['email']) == False:
            return json.dumps({'registered' : 'Email is already in use'})
        salt = ''.join(random.sample(string.ascii_letters, 8))
        connector.setSalt(data['login'], salt)
        connector.addResetKey(data['login'], "tmp")
        m = hashlib.sha256()
        m.update(salt)
        m.update(data['password'])
        password = m.hexdigest()
        for i in range(1, 2):
            m = hashlib.sha256()
            m.update(salt)
            m.update(data['password'])
            password = m.hexdigest()
        result = connector.addUserToDB(data['login'], password, data['email'], data['name'], data['surname'])
        if result == True:
            sendMail(data['email'], "Welcome!", "You have been successful registered in our application. Remember, You can reset your password only with this e-mail.")
        return json.dumps({'registered' : result})
	

class Notes:
    def GET(self, arg):
        result = connector.getUserNotes(str(arg))
        try:
            if connector.logged(web.cookies().get('sessionId')) == False:
                return web.notfound()
            connector.updateSession(web.cookies().get('sessionId'))
            web.setcookie('sessionId', web.cookies().get('sessionId'), 3600, secure=True )
            return json.dumps(result)
        except AttributeError:
            return web.notfound()
    def POST(self, arg):
        global noteIDcounter
        data = web.data()
        try:    
            if connector.logged(web.cookies().get('sessionId')) == False:
                return web.notfound()
            connector.updateSession(web.cookies().get('sessionId'))
            web.setcookie('sessionId', web.cookies().get('sessionId'), 3600, secure=True )
        except AttributeError:
            return web.notfound()     
        data = json.loads(data)
        result = connector.addNote(str(noteIDcounter), str(data['login']), str(data['text']))
        if result == True:
            response = {'noteID' : noteIDcounter }
            return json.dumps(response)            
        else:
            return json.dumps({ 'added' : False })
        noteIDcounter += 1
			
def sendMail(sendTo, message, topic):
    sender = mail()
    sender.send(sendTo, message, topic)
    return 0

class Index:
    def GET(self):	   
        return ['Hello, World!\r\n']


wsgi.server(eventlet.wrap_ssl(eventlet.listen(('localhost', 8457)),certfile='/tmp/HMIUC/ssl/server.crt',keyfile='/tmp/HMIUC/ssl/server.key',server_side=True),app.wsgifunc())
