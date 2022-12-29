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
            "close": self.close
            # "db": self.db
        }
        self.threads = {
            'm': self.main
        }
        self.stop = False

    def performing(self):
        for line in sys.stdin:
            command = line.split()
            if command[0] in self.commands:
                if len(command) == 2:
                    self.commands[command[0]](command[1])
                else:
                    self.commands[command[0]]()
            if self.stop:
                break
        for thread in self.threads.keys():
            self.threads[thread].join()
        print("administration was closed")
    
    def start(self, mod='m'):
        self.threads[mod].start()
        print(f"thread {mod} was started")
    
    def close(self, mod='a'):
        if mod == 'a':
            self.bot.stop_bot()
            self.stop = True
        else:
            self.bot.stop_bot()

if __name__ == "__main__":
    admin = Admin()
    admin.performing()
