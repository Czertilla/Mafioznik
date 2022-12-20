import telebot
from maf import Maf
from setup import SetUp
from base import Base

bot = telebot.TeleBot("5392200451:AAETSpaOC3XepS3cqvOGz0RHjSO7I1ImKlE")
users_data = Base('u')
games_data = Base('g')

@bot.message_handler(commands=["start"])
def start(message):
    user = message.from_user
    text = users_data.sign_in(user)
    bot.send_message(user.id, text)

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.from_user.id, "Для авторизации в системе пропишите команду \n/verify")

@bot.message_handler(commands=["discard"])
def discard(message):
    users_data.discard_profile(message.from_user.id)
    bot.send_message(message.from_user.id, "Ваш профиль был удален. Чтобы создать новый, пропишите команду \n/start")

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
