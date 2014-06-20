import web

class SessionController:
    def __init__(self, app):
        db = web.database(dbn='sqlite', db='/home/stud/ficm/database/database.db')
        store = web.session.DBStore(db, 'sessions')
        self.session = web.session.Session(app, store, initializer={'logged': False, 'login':None})

    def setSession(self, login):
        try: 
            self.session.logged = True
            self.session.login = login
            web.setcookie('login', login, 3600, secure=True)
        except Exception, e:
            print "Nie udalo sie ustawic sesji" + str(e)

    def destroySession(self):
        try:
            self.session.kill()
            return True
        except Exception:
            return False     

    def isLogged(self):
        if(self.session.get('logged', False)):
            return True
        else:
            return False
        
    def getLoggedUserLogin(self):
        return self.session.login
