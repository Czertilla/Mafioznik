import sqlite3
import clock
import phrases

class Base:
    def __init__(self, code, outer=None):
        self.mode = {'u': "profiles", 'g': "sessions"}[code]
        self.outer = outer
        try:
            if self.mode == 'profiles':
                self.colums = ('id', 'username', 'first_name', 'last_name',
                'language_code', 'status', 'reputation', 'registered', 'curent server', 'nav')
                self.base_name = 'users'
                # self.con = sqlite3.connect("db/users.db", check_same_thread=False)
            elif self.mode == 'sessions':
                self.colums = ('id', 'host', 'status', 'key', 'players', 'chat_link', 'setup_code', 'started', 'closed')
                self.base_name = 'games'
                # self.con = sqlite3.connect("db/games.db", check_same_thread=False)
        except Exception as e:
                return f"An attempt to connect to the database {self.mode} failed: \n\t {e}" 

    def execute(self, request, values):
        try:
            with sqlite3.connect(f"db/{self.base_name}.db", timeout=30) as con:
                cur = con.cursor()
                result = cur.execute(request, values)
                con.commit()
            return result
        except Exception as e:
            print(f"Some exception: {e}")
            self.execute(request, values)

    def fetc(self, id):
        data = self.execute(f"SELECT * FROM {self.mode} WHERE id=?", (id, ))
        data = data.fetchone()
        answer = {}
        r = 0
        for col in self.colums:
            answer[col] = data[r]
            r += 1
        return answer
    
    def search(self, what, where=False, only_whole=False, sample=False):
        if not where:
            where = self.mode
        if not sample:
            sample = self.colums
        elif type(sample) == str:
            sample = (sample, )
        result = {'whole': [], 'part': []}
        for col in sample:
            whole = self.execute(f"SELECT * FROM {where} WHERE {col}=?", (what, ))
            whole = whole.fetchall()
            while len(whole) > 0 and not whole is None:
                result['whole'].append(whole.pop(0))
            if not only_whole:
                part = self.execute(f"SELECT * FROM {where} WHERE {col} LIKE %?%", (what, ))
                part = part.fetchall()
                while len(part) > 0 and not part is None:
                    if not part in result['whole']:
                        result['part'].append(part[0])
        return result
    
    def update(self, id, col, value):
        self.execute(f"UPDATE {self.mode} SET {col} =? WHERE id =?", (value, id))

    def verify(self, id, loc=None):
        if loc is None:
            loc = self.mode
        id = id
        id = self.execute(f"SELECT * FROM {loc} WHERE id=?", (id, ))
        return not id.fetchone() is None
    
    def check_access_lvl(self, id, lvl=0):
        user = self.fetc(id)
        if lvl >= 100:
            return user["status"] == "god"
        if lvl >= 10:
            return user["status"] != "bunned"

    #only profiles
    def sign_in(self, user):
        if self.verify(user.id):
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
        print(f"new profile, id={id}")
        self.execute("INSERT INTO profiles (id, username, first_name, last_name,\
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
    
    #only profiles    
    def update_profile(self, id, request=dict):
        if 'telegram_origin' in request:
            user = vars(request.pop('telegram_origin'))
            for col in user:
                if col in self.colums:
                    self.update(id, col, user[col])
        for col in request.keys():
            print(f"UPDATE profiles SET {col} = {request[col]} WHERE id =?", (id, ))
            self.execute(f"UPDATE profiles SET {col} =? WHERE id =?", (request[col], id))
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
        self.execute("DELETE FROM profiles WHERE id =?", (id, ))
    
    #only sessions
    def new_session(self, ses):
        self.execute("INSERT INTO sessions (id, host, status, key,\
         players, chat_link, setup_code, started) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                ses.id,
                ses.host,
                ses.status,
                ses.key,
                str(ses.players)[1:-1],
                ses.chat_link,
                ses.setup_code,
                ses.started
            ))
    
    #only sessions
    def update_session(self, id, request=dict):
        # if 'telegram_origin' in request:
        #     user = vars(request.pop('telegram_origin'))
        #     for col in user:
        #         if col in self.colums:
        #             self.update(id, col, user[col])
        for col in request.keys():
            print(f"UPDATE sessions SET {col} = {request[col]} WHERE id =?", (id, ))
            self.execute(f"UPDATE sessions SET {col} =? WHERE id =?", (request[col], id))
        ses = self.fetc(id)
        closed = ses['closed']
        status = ses['status']
        if closed != None and status != 'closed':
            self.update_session(id, {'status': 'closed'})
            print(f"Some problem with data have detected during checking session:{ses['id']} status, need to check")
            if self.outer is None:
                return None
            self.outer.problems += 1
        elif closed == None and status == 'closed':
            print(f"Some problem with data have detected during checking session:{ses['id']} status")
            if self.outer is None:
                return None
            self.outer.problems += 1
        

if __name__ == "__main__":
    debug = Base("u")
    debug.fetc(715648962)

    