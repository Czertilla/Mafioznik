import sqlite3
import clock

class Base:
    def __init__(self, code):
        self.mode = {'u': "profiles", 'g': "sessions"}[code]
        if self.mode == 'profiles':
            self.con = sqlite3.connect("db/users.db", check_same_thread=False)
            self.cur = self.con.cursor()
        elif self.mode == 'sessions':
            self.con = sqlite3.connect("db/games.db", check_same_thread=False)
            self.cur = self.con.cursor()
    
    def verify(self, object):
        id = object.id
        id = self.cur.execute(f"SELECT * FROM {self.mode} WHERE id=?", (id, ))
        return not id.fetchone() is None

    def sign_in(self, user):
        if self.verify(user):
            return f"С возвращением, {user.first_name}!"
        else:
            self.new_profile(user)
            return f"Добро пожаловать, {user.first_name}!"
    
    def new_profile(self, user):
        id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        language_code = user.language_code
        registered = clock.now()
        if id == 715648962:
            status = "god"
        else:
            status = "simple"
        self.cur.execute("INSERT INTO profiles (id, username, first_name, last_name,\
            language_code, status, reputation, registered) VALUES \
            (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                id, 
                username, 
                first_name, 
                last_name, 
                language_code,
                status, 
                0.0, 
                registered
            ))
        self.con.commit()

    def discard_profile(self, id):
        self.cur.execute("DELETE FROM profiles WHERE id =?", (id, ))
        self.con.commit()