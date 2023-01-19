import uuid
import base
import clock

class Session:
    def __init__(self, host, id='', key=''):
        self.expections = []
        self.games_data = base.Base('g')
        if id:
            self.id = id
            self.refresh()
        else:
            self.generate_id()
            self.host = host
            self.status = 'lobby'
            self.key = key
            self.players = []
            self.chat_link = ''
            self.setup_code = 'STOCK'
            self.started = clock.now()
        if not 'was closed' in self.expections or \
        not 'not exist' in self.expections:
            self.setup()

    def generate_id(self):
        self.id = uuid.uuid4()
        while self.games_data.verify(self):
            self.id = uuid.uuid4()
    
    def refresh(self):
        if not self.games_data.verify(self):
            self.expections.append('not exist')
        else:
            data = self.games_data.fetch(id)
            if not data['closed'] is None:
                self.host = data['host']
                self.status = data['status']
                self.key = data['key']
                self.players = data['players']
                self.chat_link = data['chat_link']
                self.setup_code = data['setup_code']
                self.started = data['started']
            else:
                self.expections.append('was closed')

    def setup(self):
        if not self.games_data.verify(self):
            self.expections.append('not exist')

    
