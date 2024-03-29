import sys
import threading
import time

import main
from base import Base


class Admin:
    def __init__(self):
        self.bot = main.Mafioznik("5392200451:AAETSpaOC3XepS3cqvOGz0RHjSO7I1ImKlE")
        self.users_data = Base('u', self)
        self.games_data = Base('g', self)
        self.main = threading.Thread(target=self.bot.main, args=(self.users_data, self.games_data))
        self.commands = {
            "start": self.start,
            "close": self.close,
            "ban_wave": self.ban_wave,
            "search": self.search
        }
        self.threads = {
            'm': self.main
        }
        self.stop = False
        self.threshold = -12
        self.problems = 0

    def performing(self):
        for line in sys.stdin:
            try:
                spot = line.find(' ')
                command = line[:spot]
                var = line[-1:].split()
                self.commands[command](*var)
            except Exception as e:
                print(f"some problem: {e}")
                self.problems += 1
            finally:
                if self.stop:
                    break
        for thread in self.threads.keys():
            try:
                self.threads[thread].join()
            except Exception as e:
                print(f"some problem: {e}")
                self.problems += 1
        print(f"administration was closed with {self.problems} problems during work")
    
    def start(self, mod='m'):
        self.threads[mod].start()
        print(f"thread {mod} was started")
    
    def close(self, mod='a'):
        print("wait..")
        if mod == 'a':
            self.bot.stop_bot()
            self.stop = True
        else:
            self.bot.stop_bot()
    
    def ban_wave(self, change=None):
        if change != None:
            threshold = change
        else:
            threshold = self.threshold
        id_list = self.users_data.execute("SELECT id FROM profiles where reputation<?", (threshold, ))
        id_list = id_list.fetchall()
        for id in id_list:
            self.users_data.execute(f"UPDATE profiles SET status=? WHERE id=?", ('banned', id[0]))
        print(f"{len(id_list)} users was banned")
    
    def search(self, var=list):
        pass
        # what = None

        # d = {

        # }
        # for i in var:
        #     if '=' in i:
        #         pos=i[:'=']
        #         val=i['='+1]
        # print(self.users_data.search(request))
        # print(self.users_data.search(request))
        

if __name__ == "__main__":
    admin = Admin()
    admin.performing()
