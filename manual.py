import main
import sys
import time
import threading
from base import Base

class Admin:
    def __init__(self):
        self.bot = main.Mafioznik("5392200451:AAETSpaOC3XepS3cqvOGz0RHjSO7I1ImKlE")
        self.users_data = Base('u')
        self.games_data = Base('g')
        self.main = threading.Thread(target=self.bot.main, args=(self.users_data, self.games_data))
        self.commands = {
            "start": self.start,
            "close": self.close,
            "ban_wave": self.ban_wave
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
                command = line.split()
                if command[0] in self.commands:
                    if len(command) == 2:
                        self.commands[command[0]](command[1])
                    else:
                        self.commands[command[0]]()
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
    
    def find(self):
        pass

if __name__ == "__main__":
    admin = Admin()
    admin.performing()
