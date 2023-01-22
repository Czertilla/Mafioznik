import uuid
import base
import clock

class Session:
    def __init__(self, host, id=None, key=''):
        self.expections = []
        self.games_data = base.Base('g')
        if id:
            self.id = id
            self.refresh()
            self.init_vars()
            return None
        else:
            self.generate_id()
            self.host = host
            self.status = 'lobby'
            self.key = key
            self.players = []
            self.chat_link = ''
            self.setup_code = 'STOCK'
            self.started = clock.now()
            self.closed = None
            self.init_vars()
        if 'was closed' in self.expections:
            return 'was closed'
        if 'not exist' in self.expections:
            return 'not exist'
        self.games_data.new_session(self)
    
    def init_vars(self):
        self.vars = {
            'id': self.id,
            'host': self.host,
            'status': self.status,
            'key': self.key,
            'players': self.players,
            'chat_link': self.chat_link,
            'setup_code': self.setup_code,
            'started': self.started,
            'closed': self.closed
        }

    def update(self, request=dict):
        for var in request.keys():
            self.vars[var] = request[var]
        self.games_data.update_session(self.id, request)

    def generate_id(self):
        self.id = str(uuid.uuid4())
        while self.games_data.verify(self.id):
            self.id = uuid.uuid4()
    
    def refresh(self):
        if not self.games_data.verify(self.id):
            self.expections.append('not exist')
        else:
            data = self.games_data.fetc(self.id)
            if data['closed'] is None:
                self.host = data['host']
                self.status = data['status']
                self.key = data['key']
                self.players = data['players']
                self.chat_link = data['chat_link']
                self.setup_code = data['setup_code']
                self.started = data['started']
                self.closed = data['closed']
            else:
                self.expections.append('was closed')

    def setup(self):
        if not self.games_data.verify(self.id):
            self.expections.append('not exist')
    
    def close(self):
        request = {
            'closed': clock.now(),
            'status': 'closed'
        }
        self.update(request)
        del self
