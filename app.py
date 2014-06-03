# -*- coding: utf-8
#!/usr/bin/python
"""A web.py application powered by gevent"""
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
import time
import os
import sqlite3

database = "database.db"

def connect():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    return conn, c
	
def getLastID():
    conn, cursor = connect()
    cursor.execute("select id from notes;")
    ids = cursor.fetchall()
    lastID = 0
    conn.close()
    for id in ids:
        tmp = id[0]
        if tmp > lastID:
            lastID = tmp
    return lastID

noteIDcounter = getLastID()
	
def addFile(login, userFile):
    conn, cursor = connect()
    conn.close()
    return 0
def addNote(noteID, login, note):
    conn, cursor = connect()
    try:
        cursor.execute("insert into notes values(\'"+noteID+"\',\'"+login+"\',\'"+note+"\');")
    except sqlite3.IntegrityError:
        return False
    conn.commit()
    conn.close()
    noteIDcounter += 1
    return True
	
def getUserNotes(login):
    conn, cursor = connect() 
    try:
        cursor.execute("select note from notes where login=\'"+login+"\';")
        rows = cursor.fetchall()
	if len(rows) == 0:
            return []
        else:
            response = []
            for row in rows:
                response.append(row[0])
            return response
    except sqlite3.IntegrityError:
        return []
	
def getUserFile( login ):
    conn, cursor = connect()
    conn.close()
    return 0
	
def getUserInformation(login):
    conn, cursor = connect()
    cursor.execute("select * from users where login=\'"+login+"\';")
    info = cursor.fetchone()
    conn.close()
    return info
	
def checkPassword( login, password):
    conn, cursor = connect()
    cursor.execute('select password from users where login=\'' + login + "\';")
    result = cursor.fetchone()
    conn.close()
    result = result[0]
    if result == password:
        return True
    return False
	
def addErrorLog( date, message):
    conn, cursor = connect()
    conn.close()
    return 0
	
def addLog( date, message):
    conn, cursor = connect()
    conn.close()
    return 0
	
def checkIfLoginIsFree(login):
    conn, cursor = connect()
    cursor.execute("select login from users where login=\'"+login+"\';")
    rows = cursor.fetchone()
    conn.close()
    result = rows[0]
    if result == login:
        return False
    return True
def addUserToDB( login, password, email, name, surname):
    conn, cursor = connect()
    try:
        cursor.execute("insert into users values(\'"+login+"\',\'"+password+"\',\'"+email+"\',\'"+name+"\',\'"+surname+"\');")
    except sqlite3.IntegrityError:
        return False
    conn.commit()
    conn.close()
    return True
if __name__ == "__main__":
    print getUserInformation('python')