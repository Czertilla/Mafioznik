import sys
import threading

import telebot

import phrases
from base import Base
from maf import Maf
from session import Session
from setup import SetUp


class Mafioznik(telebot.TeleBot):
    def ses_init(self):
        self.sessions = {}
    
    def get_user(self, message):
        id = message.from_user.id
        user = self.users_data.fetc(id)
        return user
    
    def get_session(self, ses_id=None, key=None, host=None):
        if not ses_id in self.sessions:
            ses = Session(key=key, id=ses_id, host=host)
            self.sessions[ses.id] = ses
            ses_id = ses.id
        return self.sessions[ses_id]
    
    def get_command(self, message):
        if type(message) == str:
            text = message
        else:
            text = message.text
        spot = text.find(' ')
        command = text[:spot]
        var = text[spot:]
        return (command, var)


    def main(self, users_data, games_data):
        self.users_data = users_data
        self.games_data = games_data
        self.ses_init()

        @self.message_handler(commands=["start"])
        def start(message):
            user = message.from_user
            text = users_data.sign_in(user)
            self.send_message(user.id, text)

        @self.message_handler(commands=["help"])
        def help(message):
            user = self.get_user(message)
            nav = user['nav']
            lang = user['language_code']
            self.send_message(message.from_user.id, phrases.helping(nav)[lang])

        @self.message_handler(commands=["language"])
        def language(message):
            user = self.get_user(message)
            lang = user['language_code']
            lang_list = telebot.types.InlineKeyboardMarkup()
            for code in phrases.language_codes:
                lang_list.add(telebot.types.InlineKeyboardButton(text = phrases.languages[code], \
                    callback_data = f"{code} cl"))
            self.send_message(user['id'], phrases.lang_list()[lang], reply_markup=lang_list)

        @self.callback_query_handler(func=lambda call: 'cl' in call.data)
        def change_language(call):
            self.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            call.message.from_user.first_name
            code = call.data.split()[0]
            id = call.message.chat.id
            users_data.update_profile(id, {'language_code': code})
            self.send_message(id, phrases.commit('cl')[code])

        @self.message_handler(commands=["connect"])
        def connect(message):
            self.send_message(message.from_user.id, 'Currently not available')
        
        @self.message_handler(commands=["new_session"])
        def new_session(message, password=None, ses_id=None):
            if ses_id is None or not ses_id in self.sessions:
                user = self.get_user(message)
                id = user['id']
                if password is None and ses_id is None:
                    command = message.text
                    spot = command.find(' ')
                    password = command[spot:]
                ses = self.get_session(key=password, ses_id=ses_id, host=id)
                request = {'nav': f"hs/{ses.id}"}
                users_data.update_profile(id, request)
            session_menu(message, ses_id)
            
        @self.message_handler(commands=["create"])
        def create(message):
            user = self.get_user(message)
            id = user['id']
            request = {'nav': 'ss'}
            users_data.update_profile(id, request)
            lang = user['language_code']
            autosearch = games_data.search(id, sample='host', only_whole=True)
            sessions = []
            for i in autosearch['whole']:
                ses = games_data.fetc(i[0])
                if ses['status'] != 'closed':
                    sessions.append(ses)
            ses_list = telebot.types.InlineKeyboardMarkup()
            for s in sessions:
                ses_list.add(
                    telebot.types.InlineKeyboardButton(text = f"{s['started']}, {s['status']}",
                    callback_data = f"{s['id']} hs")
                    )
            ses_list.add(
                telebot.types.InlineKeyboardButton(text = phrases.add_new_session()[lang],
                    callback_data = f"new hs")
            )
            self.send_message(user['id'], phrases.ses_list()[lang], reply_markup=ses_list)
        
        @self.callback_query_handler(func=lambda call:'hs' == call.data[-2:])
        def session_select_interactive(call):
            self.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            user = self.get_user(call)
            id = user['id']
            command = call.data.split()[0]
            request = {'nav': f'hs/{command}'}
            users_data.update_profile(id, request)
            lang = user['language_code']
            if command == 'new':
                session_privacy(call)
            else:
                new_session(call, ses_id=command)
        
        @self.callback_query_handler(func=lambda call:'mo' == call.data[-2:])
        def make_open(call):
            tail = (call.message.chat.id, call.message.message_id)
            call.text = ''
            set_password(call, tail)

        @self.message_handler(commands=["session_menu"])
        def session_menu(message, ses_id=None):
            user = self.get_user(message)
            lang = user['language_code']
            ses_menu = telebot.types.InlineKeyboardMarkup()
            ses_menu.add(telebot.types.InlineKeyboardButton(text=phrases.session_multiplayer()[lang],\
                callback_data=f"sm {ses_id} mp"))
            ses_menu.add(telebot.types.InlineKeyboardButton(text=phrases.session_privacy()[lang],\
                callback_data=f"sm {ses_id} sp"))
            ses_menu.add(telebot.types.InlineKeyboardButton(text=phrases.session_close()[lang],\
                callback_data=f"sm {ses_id} sc"))
            self.send_message(user['id'], phrases.ses_menu(ses_id)[lang], reply_markup=ses_menu)

        @self.callback_query_handler(func=lambda call:'sm' == call.data[:2])
        def session_menu_intaractive(call):
            self.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            menu, var = self.get_command(call.data)
            ses_id, command = var.split()
            {
                'mp': session_multiplayer_menu,
                'sp': session_privacy,
                'sc': session_close
            }[command](call, ses_id)
        
        @self.message_handler(commands=["session_multiplayer"])
        def session_multiplayer_menu(message, ses_id=None):
            if ses_id is None:
                var = self.get_command(message)[1].split()
                ses_id = var[0]
                if ses_id == '':
                    return None
                if var[-1] == 'm':
                    session_multiplayer_intaractive(call=f"{ses_id}m")
                elif var[-1] == 's':
                    session_multiplayer_intaractive(call=f"{ses_id}s")
                else:
                    session_multiplayer_menu(message, ses_id=ses_id)
            else:
                user = self.get_user(message)
                lang = user['language_code']
                ses = self.get_session(ses_id)
                menu = telebot.types.InlineKeyboardMarkup()
                menu.add(telebot.types.InlineKeyboardButton(text=phrases.session_mp_mode('m')[lang],\
                callback_data=f"mpm/sm {ses_id} m"))
                menu.add(telebot.types.InlineKeyboardButton(text=phrases.session_mp_mode('s')[lang],\
                callback_data=f"mpm/sm {ses_id} s"))
                self.send_message(user['id'], phrases.set_mp_mode(ses.multiplayer)[lang], reply_markup=menu)
        
        @self.callback_query_handler(func=lambda call:'mpm/sm' == call.data[:6])
        def session_multiplayer_intaractive(call):
            self.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            if type(call) == str:
                mode = call[-1] == 'm'
                ses_id = call[:-1]
            else:
                mode = call.data[-2:] == 'm'
                ses_id = call.data[7:-2]
            ses = self.get_session(ses_id)
            ses.update({'multiplayer': mode})
            
        @self.message_handler(commands=["session_privacy"])
        def session_privacy(message, ses_id='new'):
            user = self.get_user(message)
            id = user['id']
            command = message.data.split()[0]
            nav = user['nav'].split('/')
            if not nav[-1] == ses_id:
                return None
            request = {'nav': f"{user['nav']}/sp"}
            users_data.update_profile(id, request)
            lang = user['language_code']
            menu = telebot.types.InlineKeyboardMarkup()
            menu.add(telebot.types.InlineKeyboardButton(
                text=phrases.open_pass()[lang], callback_data=f"{ses_id} mo"))
            self.send_message(user['id'], phrases.select_password()[lang], reply_markup=menu)
        
        @self.message_handler(commands=["session_close"])
        def session_close(message, ses_id=None):
            if ses_id is None:
                ses_id = self.get_command(message)[1]
                if ses_id == '':
                    return None
            else:
                user = self.get_user(message)
                if not ses_id in user['nav']:
                    return None
            self.sessions.pop(ses_id).close()

        @self.message_handler(commands=["main"])
        def main(message):
            user = self.get_user(message)
            id = user['id']
            request = {'nav': 'mm'}
            users_data.update_profile(id, request)
            lang = user['language_code']
            menu = telebot.types.InlineKeyboardMarkup()
            menu.add(telebot.types.InlineKeyboardButton(text=phrases.main_menu("connect")[lang],\
                callback_data="connect mm"))
            menu.add(telebot.types.InlineKeyboardButton(text=phrases.main_menu("create")[lang],\
                callback_data="create mm"))
            menu.add(telebot.types.InlineKeyboardButton(text=phrases.main_menu("profile")[lang],\
                callback_data="profile mm"))
            self.send_message(user['id'], phrases.main_menu()[lang], reply_markup=menu)

        @self.callback_query_handler(func=lambda call:'mm' in call.data)
        def main_menu_interactive(call):
            self.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            command = call.data.split()[0]
            {
                'connect': connect,
                'create': create,
                'profile': profile
            }[command](call)

        @self.message_handler(commands=["profile"])
        def profile(message):
            user = self.get_user(message)
            id = user['id']
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
            self.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            command = call.data.split()[0]
            {
                'update': update,
                'stats': stats,
                'language': language,
                'discard': discard
            }[command](call)

        @self.message_handler(commands=["stats"])
        def stats(message):
            user = self.get_user(message)
            lang = user['language_code']
            self.send_message(id, phrases.stats(user)[lang])

        @self.message_handler(commands=["update"])
        def update(message):
            user = message.from_user
            users_data.update_profile(user.id, {'telegram_origin': user})
            user = users_data.fetc(user.id)
            self.send_message(user['id'], phrases.commit('pu')[user['language_code']])

        @self.message_handler(commands=["discard"])
        def discard(message):
            user = self.get_user(message)
            name = users_data.fetc(id)['first_name']
            lang = message.from_user.language_code
            mesg = self.send_message(id, phrases.confirm(name)[lang])
            self.register_next_step_handler(mesg, discard_fork)

        def discard_fork(message):
            user = self.get_user(message)
            name = message.from_user.first_name
            lang = message.from_user.language_code
            if message.text == name:
                users_data.discard_profile(message.from_user.id)
                self.send_message(id, phrases.after_discard()[lang])
        
        @self.message_handler(content_types=['text'])
        def set_password(message, tail=None):
            if tail is None:
                tail = (message.chat.id, message.message_id-1)
            user = self.get_user(message)
            nav = user['nav'].split('/')
            if nav[-1] != 'sp':
                return None
            password = message.text
            self.delete_message(chat_id=tail[0], message_id=tail[1])
            ses_id = nav[-2]
            request = {'key': password}
            if ses_id == 'new':
                new_session(message, password=password)
            elif ses_id in self.sessions:
                self.sessions[ses_id].update(request)
            elif games_data.verify(ses_id):
                games_data.update_session(ses_id, request)
                new_session(message, ses_id=ses_id)
            

        # @self.message_handler(commands=["close_bot"])
        # def close_bot(message):
        #     user = self.get_user(message)
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
