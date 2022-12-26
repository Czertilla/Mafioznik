import telebot
from maf import Maf
from setup import SetUp
from base import Base
import sys
# from admin import Admin
import phrases

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
    id = message.from_user.id
    user = users_data.fetc(id)
    nav = user['nav']
    lang = user['language_code']
    bot.send_message(message.from_user.id, phrases.helping(nav)[lang])

@bot.message_handler(commands=["language"])
def language(message):
    id = message.from_user.id
    user = users_data.fetc(id)
    lang = user['language_code']
    lang_list = telebot.types.InlineKeyboardMarkup()
    for code in phrases.language_codes:
        lang_list.add(telebot.types.InlineKeyboardButton(text = phrases.languages[code], \
            callback_data = code + ' cl'))
    bot.send_message(user['id'], phrases.lang_list()[lang], reply_markup=lang_list)

@bot.callback_query_handler(func=lambda call: 'cl' in call.data)
def change_language(call):
    call.message.from_user.first_name
    code = call.data.split()[0]
    id = call.message.chat.id
    users_data.update_profile(id, {'language_code': code})


@bot.message_handler(commands=["main"])
def main(message):
    id = message.from_user.id
    user = users_data.fetc(id)
    request = {'nav': 'mm'}
    users_data.update_profile(id, request)

@bot.message_handler(commands=["profile"])
def profile(message):
    id = message.from_user.id
    user = users_data.fetc(id)
    request = {'nav': 'pm'}
    users_data.update_profile(id, request)
    lang = user['language_code']
    menu = telebot.types.InlineKeyboardMarkup()
    menu.add(telebot.types.InlineKeyboardButton(text=phrases.profile_menu("update")[lang],\
         callback_data="update pm"))
    menu.add(telebot.types.InlineKeyboardButton(text=phrases.profile_menu("stats")[lang],\
        callback_data="stats pm"))
    menu.add(telebot.types.InlineKeyboardButton(text=phrases.profile_menu("language")[lang],\
        callback_data="language pm"))
    menu.add(telebot.types.InlineKeyboardButton(text=phrases.profile_menu("discard")[lang],\
        callback_data="discard pm"))
    bot.send_message(user['id'], phrases.profile_menu()[lang], reply_markup=menu)
    
@bot.callback_query_handler(func=lambda call:'pm' in call.data)
def profile_menu_interactive(call):
    command = call.data.split()[0]
    {
        'update': update,
        'stats': stats,
        'language': language,
        'discard': discard
    }[command](call)

@bot.message_handler(commands=["stats"])
def stats(message):
    id = message.from_user.id
    user = users_data.fetc(id)
    lang = user['language_code']
    bot.send_message(id, phrases.stats(user)[lang])

@bot.message_handler(commands=["update"])
def update(message):
    user = message.from_user
    users_data.update_profile(user.id, {'user': user})

@bot.message_handler(commands=["discard"])
def discard(message):
    id = message.from_user.id
    name = users_data.fetc(id)['first_name']
    lang = message.from_user.language_code
    mesg = bot.send_message(id, phrases.confirm(name)[lang])
    bot.register_next_step_handler(mesg, discard_fork)

def discard_fork(message):
    id = message.from_user.id
    name = message.from_user.first_name
    lang = message.from_user.language_code
    if message.text == name:
        users_data.discard_profile(message.from_user.id)
        bot.send_message(id, phrases.after_discard()[lang])


bot.polling(none_stop=True, interval=0)
# SetUp()
# Game = input("Press <<Enter>> to start ")
# if not Game:
#     Game = Maf()
#     Game.start()
#     Game.end()  
