import sqlite3

database = "/home/stud/ficm/database/database.db"

def connect():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    return conn, c
		
class dbConnector:
    def __init__(self):
        return
    		
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
if __name__ == "__main__":
    dbConnector = dbConnector()
    print dbConnector.getSalt("test")
