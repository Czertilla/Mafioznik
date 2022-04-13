class Player:
    def __init__(self, nick, role):
        self.nick = nick
        self.hp = 1
        self.role = role
        self.caste = self.set_caste()
        self.next_night()
        self.detected = False
        self.stats = {
            "kills": 0,
            "deads": 0,
            "saves": 0,
            "wins": 0
            }  
    
    def set_caste(self):
        ghost = {'host', 'outlaw', 'corpse'}
        criminal = {'mafia', 'mistress'}
        peaceful = {'civil', 'tec', 'doc', 'lawyer', 'bodyguard'}
        renegade = {'maniac'}
        if self.role in ghost:
            return "ghost"
        if self.role in criminal:
            return "criminal"
        if self.role in peaceful:
            return "peaceful"
        if self.role in renegade:
            return "renegade"        
    
    def next_night(self):
        self.hp = int(bool(self.hp))
        self.target = None
        self.erection = False
        self.alibi = False
        self.vote_weight = int(self.caste != "ghost")
