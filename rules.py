import copy
from random import randint


class Rules:    
    def __init__(self, outer):
        #settings---------------------------------------------------------------
        self.AHFM =                                                        True
        self.mistress = 'mistress' in outer.roles
        self.lawyer =   'lawyer' in outer.roles
        self.bodyguard ='bodyguard' in outer.roles  
        self.maniac =   'maniac' in outer.roles         
        #-----------------------------------------------------------------------
        self.black_list = []
        self.castes = {"peaceful": [], "criminal": [], 
                       "renegade": [], "ghost": []}
        for player in outer.players:
            self.castes[outer.players[player].caste].append(player)
        self.mafia_count = len(self.castes["criminal"]) - int(self.mistress)            
        self.tp = copy.deepcopy(outer.nicks)
        self.setTHEorder(outer)
        self.black_list = []
    
    def setTHEorder(self, outer):
        self.order = []
        self.order.append(self.findTHEmistress(outer))
        self.order.append(self.findTHEdoc(outer))
        for i in range(self.mafia_count):
            self.order.append(self.findTHEmafia(outer))
        self.order.append(self.findTHEtec(outer))
        self.order.append(self.findTHElawyer(outer))
        self.order.append(self.findTHEmaniac(outer))
        self.order.append(self.findTHEbodyguard(outer))
        self.order = tuple(self.order)
    
    def checkTHElucker(self, d):
        dic = copy.deepcopy(d)
        if not dic:
            return "No one"
        m = max(dic.items(), key=lambda x: x[1])
        if len(dic.keys()) == 1:
            return m[0]
        dic[m[0]] = 0
        if max(dic.items(), key=lambda x: x[1])[1] == m[1]:
            return "No one"
        return m[0]
    
    def checkTHEwinner(self, players):
        if len(players) - len(self.castes["ghost"]) <= 2 and \
           len(self.castes["renegade"]) >= 1:
            return "renegade"
        if len(self.castes["criminal"]) >= len(self.castes["peaceful"]):
            return "criminal"
        if len(players) - len(self.castes["ghost"]) <= len(self.castes\
                                                           ["peaceful"]):
            return "peaceful"
        return ''

    def play_day(self, outer):
        self.black_list = []
        self.winner = self.checkTHEwinner(outer.players)
        if self.winner:
            outer.game = False
            return None
        outer.diary.write("\tVoting:\n")
        lucker = ''
        cont = False
        while not cont:
            table = {}
            for turn in outer.players.values():
                if turn.caste != "ghost":
                    choise = input(turn.nick + '?  ')
                    if choise:
                        check = choise in outer.players and \
                            outer.players[choise].caste != "ghost"
                        while not check:
                            choise = input("\tYou cannot vote for"+ \
                                       "this person, so? ")
                            check = choise in outer.players and \
                                        outer.players[choise].caste != "ghost"
                        choise = outer.players[choise]    
                        line = "\t\t"+ str(turn.nick)+ " ("+ str(turn.role)\
                                +", vote weight is "\
                                + str(turn.vote_weight)\
                                +") voted for "+ str(choise.nick)+ " ("\
                                + str(choise.role)+ ")\n"
                        outer.diary.write(line)
                        print(line, end='')
                        if choise.nick in table and not choise.alibi:
                            table[choise.nick] += turn.vote_weight
                        elif not choise.alibi:
                            table[choise.nick] = turn.vote_weight
                        else:
                            line = "\t\tBut this fucker had an alibi\n"
                            outer.diary.write(line)
                            print(line, end='')
            lucker = self.checkTHElucker(table)
            line = str(table)+ "\n\t"+ lucker+ " was exiled\n"    
            outer.diary.write(line)
            print(line, end='')
            cont = not bool(input("Continue? "))
        if lucker != "No one":
            self.eliminate(outer.players[lucker])
    
    def eliminate(self, target):
        if target.role == "mafia":
            self.mafia_count -= 1
        if target.hp:    
            target.role = ("outlaw")
        else:    
            target.role = ("corpse")
        self.castes[target.caste].pop(self.castes[target.caste].index(target.\
                                                                      nick))
        self.castes["ghost"].append(target.nick)
        target.caste = "ghost"
        target.vote_weight = 0
    
    def next_night(self, outer):
        for turn in outer.players.values():
            turn.next_night()
    
    def play_night(self, outer):
        self.next_night(outer)
        self.black_list = []
        self.table = {}
        for turn in self.order:
            if turn and turn.caste != "ghost": 
                turn.target = input(str(turn.nick)+ " ?  ")
                check = turn.target in outer.players and outer.players[turn.\
                    target].caste != "ghost"
                while not check: 
                    turn.target = input(str(turn.nick)+ " !?  ")
                    check = turn.target in outer.players and outer.players[turn.\
                        target].caste != "ghost"
                turn.target = outer.players[turn.target]    
                line = '\t'+ str(turn.nick)+ '('+ str(turn.role)+ ") choised "+ \
                    str(turn.target.nick)+ '('+ str(turn.target.role)+ ')\n'
                outer.diary.write(line)
                print(line, end='')                
                self.night_event(turn, outer)
    
    def checkTHEcorpses(self, outer):
        i = 0
        t = 0
        while t < len(self.black_list):
            if self.black_list[t].hp:
                self.black_list.pop(self.black_list.index(self.black_list[t]))
            else:
                self.eliminate(self.black_list[t])
                t += 1
                i += 1
        if i > 1:
            line = str(len(self.black_list))+ " bodies were found this morning"+\
                str([i.nick for i in self.black_list])+ " \n"
        elif i == 1:    
            line = str(len(self.black_list))+ " body was found this morning"+\
                str([i.nick for i in self.black_list])+ " \n"            
        else:
            line = "NO bodies were found this morning\n"
        outer.diary.write(line)
        print(line, end='')
        
    def night_event(self, turn, outer):
        self.targets = {}
        opt = {
            "mafia": self.conspire, # conspire not work yet 
            "maniac": self.kill, 
            "doc": self.heal,
            "tec": self.detect,
            "mistress": self.fuck,
            "bodyguard": self.sacrifice,
            "lawyer": self.jusify
               }
        line = opt[turn.role](turn)
        if line:
            outer.diary.write(line)
            print(line, end='')                 
    
    def conspire(self, turn):
        if turn.target.role == "mafia" or turn.erection:
            self.kill(turn)
            return "Betrayal!?\n"
        self.targets[turn.target.nick] = turn.target
        if turn.target.nick in self.table:
            self.table[turn.target.nick] += int(not turn.erection)
        else:
            self.table[turn.target.nick] = int(not turn.erection)
        if sum(self.table.values()) == self.mafia_count:
            lucker = self.checkTHElucker(self.table)
            if lucker and lucker != 'No one':
                lucker = self.targets[lucker]
                turn.target = lucker
                self.kill(turn)
    
    def kill(self, turn):
        if turn.caste != "ghost" and turn.target is self.mistress and not\
             turn.target.erection:
            turn.target.hp -= int(bool(turn.target.hp))
            self.black_list.append(turn.target)            
            turn.target.target.hp -= int(bool(turn.target.target.hp)) 
            self.black_list.append(turn.target.target)
            if self.mistress.target is turn:
                turn.hp += 1
        elif turn.caste != "ghost" and not(turn.target.erection):
            turn.target.hp -= int(bool(turn.target.hp))
            self.black_list.append(turn.target)
    
    def heal(self, turn):
        if turn.caste != "ghost" and not turn.erection:
            turn.target.hp = -1
        elif turn.erection: #auto-heal for mistress
            self.mistress.hp = -1
    
    def detect(self, turn):
        if turn.caste != "ghost" and not(turn.erection or turn.target.erection):
            line = "\t\t\t"+ str(turn.target.caste)+ "\n"
        elif turn.caste != "ghost":
            a = ["peaceful", "criminal", "renegade"]
            r = randint(1, 2)
            line = "\t\t\t"+ a[a.index(turn.target.caste) - r]+ "\n"
        return line    
    
    def fuck(self, turn):
        turn.target.erection = True
        turn.target.vote_weight = 0
        
    def sacrifice(self, turn):
        if turn.erection and turn.target != self.mistress:
            turn.target = self.mistress
            self.sacrifice(turn)
            return None
        if turn.caste != "ghost" and not turn.target.erection:
            if not turn.target.hp in {-1, 1}:
                turn.target.hp += 1
                turn.hp -= 1
                if not turn in self.black_list:
                    self.black_list.append(turn)
    
    def jusify(self, turn):
        if turn.erection and turn.target != self.mistress:
            turn.target = self.mistress
            self.jusify(turn)
            return None
        if turn.caste != "ghost" and not turn.target.erection:
            turn.target.alibi = True
                
    def findTHEdoc(self, outer):
        for p in self.tp:
            if outer.players[p].role == "doc":
                self.tp.pop(self.tp.index(p))
                return outer.players[p]
    
    def findTHEmistress(self, outer):
        for p in self.tp:
            if outer.players[p].role == "mistress":
                self.mistress = outer.players[p]
                self.tp.pop(self.tp.index(p))
                return outer.players[p]  
            
    def findTHEbodyguard(self, outer):
        for p in self.tp:
            if outer.players[p].role == "bodyguard":
                self.tp.pop(self.tp.index(p))
                return outer.players[p]   
            
    def findTHEmafia(self, outer):
        for p in self.tp:
            if outer.players[p].role == "mafia":
                self.tp.pop(self.tp.index(p))
                return outer.players[p]
            
    def findTHEtec(self, outer):
        for p in self.tp:
            if outer.players[p].role == "tec":
                self.tp.pop(self.tp.index(p))
                return outer.players[p]    
            
    def findTHElawyer(self, outer):
        for p in self.tp:
            if outer.players[p].role == "lawyer":
                self.tp.pop(self.tp.index(p))
                return outer.players[p] 
            
    def findTHEmaniac(self, outer):
        for p in self.tp:
            if outer.players[p].role == "maniac":
                self.tp.pop(self.tp.index(p))
                return outer.players[p]    
