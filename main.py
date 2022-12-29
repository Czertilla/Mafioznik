import telebot
from maf import Maf
from setup import SetUp
from base import Base
import sys
import phrases
import threading

class Mafioznik(telebot.TeleBot):
    def main(self, users_data, games_data):
        @self.message_handler(commands=["start"])
        def start(message):
            user = message.from_user
            text = users_data.sign_in(user)
            self.send_message(user.id, text)

        @self.message_handler(commands=["help"])
        def help(message):
            id = message.from_user.id
            user = users_data.fetc(id)
            nav = user['nav']
            lang = user['language_code']
            self.send_message(message.from_user.id, phrases.helping(nav)[lang])

        @self.message_handler(commands=["language"])
        def language(message):
            id = message.from_user.id
            user = users_data.fetc(id)
            lang = user['language_code']
            lang_list = telebot.types.InlineKeyboardMarkup()
            for code in phrases.language_codes:
                lang_list.add(telebot.types.InlineKeyboardButton(text = phrases.languages[code], \
                    callback_data = code + ' cl'))
            self.send_message(user['id'], phrases.lang_list()[lang], reply_markup=lang_list)

        @self.callback_query_handler(func=lambda call: 'cl' in call.data)
        def change_language(call):
            call.message.from_user.first_name
            code = call.data.split()[0]
            id = call.message.chat.id
            users_data.update_profile(id, {'language_code': code})


        @self.message_handler(commands=["main"])
        def main(message):
            id = message.from_user.id
            user = users_data.fetc(id)
            request = {'nav': 'mm'}
            users_data.update_profile(id, request)

        @self.message_handler(commands=["profile"])
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
            self.send_message(user['id'], phrases.profile_menu()[lang], reply_markup=menu)
            
        @self.callback_query_handler(func=lambda call:'pm' in call.data)
        def profile_menu_interactive(call):
            command = call.data.split()[0]
            {
                'update': update,
                'stats': stats,
                'language': language,
                'discard': discard
            }[command](call)

        @self.message_handler(commands=["stats"])
        def stats(message):
            id = message.from_user.id
            user = users_data.fetc(id)
            lang = user['language_code']
            self.send_message(id, phrases.stats(user)[lang])

        @self.message_handler(commands=["update"])
        def update(message):
            user = message.from_user
            users_data.update_profile(user.id, {'user': user})

        @self.message_handler(commands=["discard"])
        def discard(message):
            id = message.from_user.id
            name = users_data.fetc(id)['first_name']
            lang = message.from_user.language_code
            mesg = self.send_message(id, phrases.confirm(name)[lang])
            self.register_next_step_handler(mesg, discard_fork)

        def discard_fork(message):
            id = message.from_user.id
            name = message.from_user.first_name
            lang = message.from_user.language_code
            if message.text == name:
                users_data.discard_profile(message.from_user.id)
                self.send_message(id, phrases.after_discard()[lang])

        # @self.message_handler(commands=["close_bot"])
        # def close_bot(message):
        #     id = message.from_user.id
        #     lang = message.from_user.language_code
        #     if users_data.check_access_lvl(id, 100):

        self.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    bot = Mafioznik("5392200451:AAETSpaOC3XepS3cqvOGz0RHjSO7I1ImKlE")
    users_data = Base('u')
    games_data = Base('g')
    bot.main(users_data, games_data)
    # SetUp()
    # Game = input("Press <<Enter>> to start ")
    # if not Game:
    #     Game = Maf()
    #     Game.start()
    #     Game.end()  
