from player import Player
from rules import Rules
from random import randint

class Maf:
    def __init__(self):
        self.roles = ["mafia",  
                      "tec", 
                      "doc",
                      "mistress",
                      "civil",
                      "bodyguard",
                      "lawyer",
                      "maniac",
                      "mafia", "mafia", "civil", "civil", "mafia", "civil", 
                      "civil", "mafia", "civil", "civil", "mafia", "civil",
                      "civil", "mafia", "civil", "civil", "mafia", "civil", 
                      "civil", "mafia", "civil", "civil", "mafia"]
        # self.roles = ["mafia", "doc", "tec", "civil", "civil", "mafia"]
        note = open("note.txt", 'r+') 
        self.note = list(note)
        self.num = int(self.note[0]) + 1
        self.note[0] = self.num
        self.nicks = []
        for i in self.note[1:]:
            self.nicks.append(i[:-1]) 
        self.diary = open("diaries/diary#" + str(self.num) + ".txt", 'w')
        self.players = {}
        self.roles = self.roles[:len(self.nicks)]    
        for nick in self.nicks:
            self.players[nick] = Player(nick, self.pickTHErole())
        self.game = True
        self.date = -1
        self.diary.write("Game #" + str(self.num)+ "\t\t"+ str(self)[19:-2]+ \
                         "\n\n")
        self.rule = Rules(self)    
    
    def pickTHErole(self):
        return self.roles.pop(randint(0, len(self.roles) - 1))
        
    def start(self):
        for player in self.players.values():
            line = "\t\t"+ player.nick+ " -- "+ player.role+ '\n'
            self.diary.write(line)
            print(line)
        while self.game:
            self.date += 1
            line = "Day " + str(self.date//2) + '\n'
            self.diary.write(line)
            print(line)      
            self.rule.checkTHEcorpses(self)
            if self.game and self.rule.castes['ghost']:          
                self.rule.play_day(self)    
            self.date += 1                 
            if self.game:      
                self.diary.write("Night " + str(self.date//2) + '\n')
                print("\nNight", self.date//2)          
                self.rule.play_night(self)    
        self.diary.write("\t\t"+ self.rule.winner + " Wins!!\t"+ \
                         str(self.rule.castes[self.rule.winner]))        
    
    def end(self):
        self.note[0] = str(self.note[0]) + '\n'
        self.game = False
        file = open("note.txt", 'w+')
        for line in self.note:
            file.write(str(line))
        file.close()    
        self.diary.close()    
