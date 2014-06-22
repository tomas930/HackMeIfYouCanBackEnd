import sqlite3
import hashlib
import random
import string
from datetime import datetime, timedelta
database = "/home/stud/ficm/database/database.db"

def connect():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    return conn, c
		
class dbConnector:
    def __init__(self):
        return
		
    def logged(self, sessionId):
        conn, cursor = connect()
        com = "select * from sessions where sessionId=?"
        cursor.execute(com, (sessionId,))
        result = cursor.fetchone()
        time = datetime.now()
        conn.close()
        if result == None:
            return False
        time = format(time, '%H:%M:%S')
        if (datetime.strptime(result[3], "%H:%M:%S") - datetime.strptime(time, '%H:%M:%S') ) < timedelta(minutes=1):
            self.killSession(sessionId)
            return False  
        return True
    def updateSession(self, sessionId):
        conn, cursor = connect()
        expire = datetime.now() + timedelta(hours=1)
        expire = format(expire, '%H:%M:%S')
        try:
            com = "update sessions set expire=\'" + str(expire) + "\' where sessionId=?"
            cursor.execute(com, (sessionId,))
            conn.commit()
            conn.close()
        except Exception:
            conn.commit()
            conn.close()
            return False
        return True
		
    def killSession(self, sessionId):
        conn, cursor = connect()
        try:
            com = "select login from sessions where sessionId=?"
            cursor.execute(com, (sessionId,))
            login = cursor.fetchone() 
            conn.commit()
            conn.close()
            conn, cursor = connect()
            print login[0]  			
            com = "delete from sessions where login=?"
            cursor.execute(com, (str(login[0]),))
        except Exception:
            return False
        conn.commit()
        conn.close()
        return True
    def setSession(self, login):
        conn, cursor = connect()
        sessionId = ''.join(random.sample(string.ascii_letters, 24))
        m = hashlib.sha256()
        m.update(sessionId)
        sessionId = m.hexdigest()
        expire = datetime.now() + timedelta(hours=1)
        expire = format(expire, '%H:%M:%S')
        # TODO: if zalogowany -> update session + return ID
        try:
            com = "insert into sessions values (?,?,?,?)"
            cursor.execute(com, (login,'true',sessionId,expire,))
        except Exception:
            return False
        conn.commit()
        conn.close()
        return sessionId
    def emailFree(self, email):
        conn, cursor = connect()
        com = "select email from users where email=?"
        cursor.execute(com, (email,))
        result = cursor.fetchone()
        conn.close()
        return result == None

    def getLoginByResetKey(self, key):
        conn, cursor = connect()
        com = "select login from resetPassword where resetKey=?"
        cursor.execute(com, (key,))
        result = cursor.fetchone()
        conn.close()
        if result == None:
            return None
        else:
            return result[0]

    def enableResetPassword(self, login):
        conn, cursor = connect()
        try:
            com = "update resetPassword set canReset=\'true\' where login=?"
            cursor.execute(com, (login,))
        except Exception:
            return False
        conn.commit()
        conn.close()
        return True
		
    def addResetKey(self, login, key):
        conn, cursor = connect()
        try:
            com = "insert into resetPassword values (?,?,?)"
            cursor.execute(com, (login,key,'false',))
        except Exception:
            return False
        conn.commit()
        conn.close()
        return True
    def canResetPassword(self, login):
        conn, cursor = connect()
        com = "select canReset from resetPassword where login=?"
        cursor.execute(com, (login,))
        result = cursor.fetchone()
        conn.close()
        if result[0] == 'false':
            return False
        return True

    def disableResetPassword(self, login):
        conn, cursor = connect()
        try:
            com = "update resetPassword set canReset=\'false\' where login=?"
            cursor.execute(com, (login,))
        except Exception:
            return False
        conn.commit()
        conn.close()
        return True

    def setSalt(self, login, salt):
        conn, cursor = connect()
        try:
            com = "insert into salts values(? ,?)"
            cursor.execute(com, (login, salt,))
        except Exception:
            return False
        conn.commit()
        conn.close()
        return True
		
    def getSalt(self, login):
        conn, cursor = connect()
        com = "select salt from salts where login=?"
        cursor.execute(com, (login,))
        result = cursor.fetchone()
        conn.close()
        print result[0]		
        return result[0]
        
		
    def getLastID(self):
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
		
    def addFile(self,login, userFile, extension):
        conn, cursor = connect()
        file = open(userFile, 'rb')
        data = file.read()
        com = "select file from files where login=?;"
        cursor.execute(com, (login,))
        result = cursor.fetchone()
        if result == None:
            com = "insert into files values( ?, ?, ?);"
            cursor.execute(com, (login, data, extension,))
        else:
            com = "update files set file=? where login=?;"
            cursor.execute(com, (data, login,))
        conn.commit()   
        conn.close()
        return True

    def getUserFile(self,login):
        conn, cursor = connect()
        com = "select file from files where login=?;"
        cursor.execute(com, (login,))
        result = cursor.fetchone()
        com = "select extension from files where login=?;"
        cursor.execute(com, (login,))
        extension = cursor.fetchone()
        conn.close()
        if result == None:
	        return None
        else:
            file = open('toDownload.' + extension, 'w')
            file.write(str(result[0]))
            file.close()
            return file
    
    def addNote(self,noteID, login, note):
        conn, cursor = connect()
        try:
            com = "insert into notes values(?, ?, ?);"
            cursor.execute(com, (noteID, login, note,))
        except sqlite3.IntegrityError:
            return False
        conn.commit()
        conn.close()
        noteIDcounter += 1
        return True
	
    def updateUserPassword(self, login, password):
        conn, cursor = connect()
        try:
            com = 'update users set password=? where login=?;'
            cursor.execute(com, (password, login,))
        except Exception:
            return False
        conn.commit()
        conn.close()
        return True
		
    def getUserNotes(self,login):
        conn, cursor = connect() 
        try:
            com = 'select note from notes where login=?'
            cursor.execute(com, (login,))
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
	
    def getUserInformation(self,login):
        conn, cursor = connect()
        com = "select * from users where login=?;"
        cursor.execute(com, (login,))
        info = cursor.fetchone()
        conn.close()
        return info
	
    def checkPassword(self, login, password):
        conn, cursor = connect()
        com = 'select password from users where login=?;'
        cursor.execute(com, (login,))
        result = cursor.fetchone()
        conn.close()
        result = result[0]
        if result == password:
            return True
        return False
	
    def addErrorLog(self, date, message):
        conn, cursor = connect()
        try:
            com = "insert into aplicationLogs values(? ,?);"
            cursor.execute(com, (date, message,))
        except sqlite3.IntegrityError:
            return False
        conn.commit()
        conn.close()
        return True
	
    def addLog( self,date, message):
        conn, cursor = connect()
        try:
            com = "insert into aplicationErrorLogs values(?, ?);"
            cursor.execute(com, (date, message,))
        except sqlite3.IntegrityError:
            return False
        conn.commit()
        conn.close()
        return True
	
    def checkIfLoginIsFree(self,login):
        conn, cursor = connect()
        com = "select login from users where login=?;"
        cursor.execute(com, (login,))
        rows = cursor.fetchone()
        conn.close()
        result = rows[0]
        if result == login:
            return False
        return True
    def addUserToDB( self,login, password, email, name, surname):
        conn, cursor = connect()
        try:
            com = "insert into users values(?,?,?,?,?);"
            cursor.execute(com, (login, password, email, name, surname,))
        except sqlite3.IntegrityError:
            return False
        conn.commit()
        conn.close()
        return True

    def incNoteIDCounter(self):
        return 0

if __name__ == "__main__":
    dbConnector = dbConnector()
    print "test"
