import telebot
# import sqlite3
from base import Base 
import threading
import time

def f(x = lambda x: x if (not x is None) else 1):
    print(type(x))




if __name__ == "__main__":
    var = None
    test = lambda x: x if (x!=None) else 1
    print(test(None))
    print(test(2))
    f(var)


# 80 циклов имитации операций ввода-вывода закончены
# Общее время работы:  2.008725881576538