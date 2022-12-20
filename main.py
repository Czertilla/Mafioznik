import telebot
from maf import Maf
from setup import SetUp
from base import Base

bot = telebot.TeleBot("5392200451:AAETSpaOC3XepS3cqvOGz0RHjSO7I1ImKlE")

@bot.message_handler(commands=["start", "help"])
def start(message):
    user = message.from_user

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    pass

bot.polling(none_stop=True, interval=0)
# SetUp()
# Game = input("Press <<Enter>> to start ")
# if not Game:
#     Game = Maf()
#     Game.start()
#     Game.end()  
