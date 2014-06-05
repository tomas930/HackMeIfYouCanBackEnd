import sqlite3

database = "database.db"

def connect():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    return conn, c
		
class dbConnector:
    def __init__(self):
        return
    		
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
		
    def addFile(self,login, userFile):
        conn, cursor = connect()
        file = open(userFile, 'rb')
        data = file.read()
        cursor.execute("select file from files where login=\'"+ login + "\';")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("insert into files values(\'"+login+"\',\'"+data+"\');")
        else:
            cursor.execute("update files set file=\'"+data+"\' where login=\'" + login +"\';")
        conn.commit()   
        conn.close()
        return True

    def getUserFile(self,login):
        conn, cursor = connect()
        cursor.execute("select file from files where login=\'"+ login + "\';")
        result = cursor.fetchone()
        conn.close()
        if result == None:
	        return None
        else:
            file = open('result', 'w')
            file.write(str(result[0]))
            file.close()
            return file
    
    def addNote(self,noteID, login, note):
        conn, cursor = connect()
        try:
            cursor.execute("insert into notes values(\'"+noteID+"\',\'"+login+"\',\'"+note+"\');")
        except sqlite3.IntegrityError:
            return False
        conn.commit()
        conn.close()
        noteIDcounter += 1
        return True
	
    def getUserNotes(self,login):
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
	
    def getUserInformation(self,login):
        conn, cursor = connect()
        cursor.execute("select * from users where login=\'"+login+"\';")
        info = cursor.fetchone()
        conn.close()
        return info
	
    def checkPassword(self, login, password):
        conn, cursor = connect()
        cursor.execute('select password from users where login=\'' + login + "\';")
        result = cursor.fetchone()
        conn.close()
        result = result[0]
        if result == password:
            return True
        return False
	
    def addErrorLog(self, date, message):
        conn, cursor = connect()
        try:
            cursor.execute("insert into aplicationLogs values(\'"+date+"\',\'"+message+"\');")
        except sqlite3.IntegrityError:
            return False
        conn.commit()
        conn.close()
        return True
	
    def addLog( self,date, message):
        conn, cursor = connect()
        try:
            cursor.execute("insert into aplicationErrorLogs values(\'"+date+"\',\'"+message+"\');")
        except sqlite3.IntegrityError:
            return False
        conn.commit()
        conn.close()
        return True
	
    def checkIfLoginIsFree(self,login):
        conn, cursor = connect()
        cursor.execute("select login from users where login=\'"+login+"\';")
        rows = cursor.fetchone()
        conn.close()
        result = rows[0]
        if result == login:
            return False
        return True
    def addUserToDB( self,login, password, email, name, surname):
        conn, cursor = connect()
        try:
            cursor.execute("insert into users values(\'"+login+"\',\'"+password+"\',\'"+email+"\',\'"+name+"\',\'"+surname+"\');")
        except sqlite3.IntegrityError:
            return False
        conn.commit()
        conn.close()
        return True