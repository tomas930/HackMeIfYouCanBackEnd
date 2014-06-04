# -*- coding: utf-8
#!/usr/bin/python
"""A web.py application powered by gevent"""
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
import time
import os
import sqlite3
import mail
import dbConnector
from dbConnector import *
from mail import *

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

connector = dbConnector()
def sendMail(sendTo, topic, message):
    sender = mail()
    sender.send(sendTo, message, topic)
    return 0

noteIDcounter = connector.getLastID()
print noteIDcounter

if __name__ == "__main__":
    print