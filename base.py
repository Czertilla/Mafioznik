import sqlite3
import clock
import phrases

class Base:
    def __init__(self, code):
        self.mode = {'u': "profiles", 'g': "sessions"}[code]
        if self.mode == 'profiles':
            self.colums = ('id', 'username', 'first_name', 'last_name',
             'language_code', 'status', 'reputation', 'registered', 'curent server', 'nav')
            self.con = sqlite3.connect("db/users.db", check_same_thread=False)
            self.cur = self.con.cursor()
        elif self.mode == 'sessions':
            self.con = sqlite3.connect("db/games.db", check_same_thread=False)
            self.cur = self.con.cursor()

    def fetc(self, id):
        data = self.cur.execute(f"SELECT * FROM {self.mode} WHERE id=?", (id, ))
        data = data.fetchone()
        answer = {}
        r = 0
        for col in self.colums:
            answer[col] = data[r]
            r += 1
        return answer
    
    def update(self, id, col, value):
        self.cur.execute(f"UPDATE {self.mode} SET {col} =? WHERE id =?", (value, id))
        self.con.commit()

    def verify(self, object):
        id = object.id
        id = self.cur.execute(f"SELECT * FROM {self.mode} WHERE id=?", (id, ))
        return not id.fetchone() is None

    #only profiles
    def sign_in(self, user):
        if self.verify(user):
            self.update_profile(user.id, {'user': user, 'nav': 'mm'})
            return f"С возвращением, {user.first_name}!"
        else:
            self.new_profile(user)
            return f"Добро пожаловать, {user.first_name}!"
    
    #only profiles
    def new_profile(self, user):
        id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        language_code = user.language_code
        if not language_code in phrases.language_codes:
            language_code = 'en'
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
    
    #only profiles    
    def update_profile(self, id, request=dict):
        if 'user' in request:
            user = vars(request.pop('user'))
            for col in user:
                if col in self.colums:
                    self.update(id, col, user[col])
        for col in request.keys():
            print(f"UPDATE profiles SET {col} = {request[col]} WHERE id =?", (id, ))
            self.cur.execute(f"UPDATE profiles SET {col} =? WHERE id =?", (request[col], id))
            self.con.commit()
        reputation = self.fetc(id)['reputation']
        status = self.fetc(id)['status']
        if reputation < -10 and status != 'banned':
            self.update_profile(id, {'status': 'banned'})
        elif reputation >= -10 and status == 'banned':
            self.update_profile(id, {'status': 'simple'})

    #only profiles
    def discard_profile(self, id):
        if id == 715648962:
            return "БОГ БЕССМЕРТЕН"
        self.cur.execute("DELETE FROM profiles WHERE id =?", (id, ))
        self.con.commit()